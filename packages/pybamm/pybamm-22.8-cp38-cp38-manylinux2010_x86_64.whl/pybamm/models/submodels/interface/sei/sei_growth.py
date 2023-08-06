#
# Class for SEI growth
#
import pybamm
from .base_sei import BaseModel


class SEIGrowth(BaseModel):
    """
    Class for SEI growth.

    Parameters
    ----------
    param : parameter class
        The parameters to use for this submodel
    reaction_loc : str
        Where the reaction happens: "x-average" (SPM, SPMe, etc),
        "full electrode" (full DFN), or "interface" (half-cell model)
    options : dict, optional
        A dictionary of options to be passed to the model.

    **Extends:** :class:`pybamm.sei.BaseModel`
    """

    def __init__(self, param, reaction_loc, options=None, cracks=False):
        super().__init__(param, options=options, cracks=cracks)
        self.reaction_loc = reaction_loc

    def get_fundamental_variables(self):
        if self.reaction == "SEI on cracks":
            if self.reaction_loc == "x-average":
                L_inner_av = pybamm.Variable(
                    "X-averaged inner SEI on cracks thickness",
                    domain="current collector",
                )
                L_inner = pybamm.PrimaryBroadcast(L_inner_av, "negative electrode")
                L_outer_av = pybamm.Variable(
                    "X-averaged outer SEI on cracks thickness",
                    domain="current collector",
                )
                L_outer = pybamm.PrimaryBroadcast(L_outer_av, "negative electrode")
            elif self.reaction_loc == "full electrode":
                L_inner = pybamm.Variable(
                    "Inner SEI on cracks thickness",
                    domain="negative electrode",
                    auxiliary_domains={"secondary": "current collector"},
                )
                L_outer = pybamm.Variable(
                    "Outer SEI on cracks thickness",
                    domain="negative electrode",
                    auxiliary_domains={"secondary": "current collector"},
                )
        elif self.reaction == "SEI":
            if self.reaction_loc == "x-average":
                L_inner_av = pybamm.standard_variables.L_inner_av
                L_outer_av = pybamm.standard_variables.L_outer_av
                L_inner = pybamm.PrimaryBroadcast(L_inner_av, "negative electrode")
                L_outer = pybamm.PrimaryBroadcast(L_outer_av, "negative electrode")
            elif self.reaction_loc == "full electrode":
                L_inner = pybamm.standard_variables.L_inner
                L_outer = pybamm.standard_variables.L_outer
            elif self.reaction_loc == "interface":
                L_inner = pybamm.standard_variables.L_inner_interface
                L_outer = pybamm.standard_variables.L_outer_interface

        if self.options["SEI"] == "ec reaction limited":
            L_inner = 0 * L_inner  # Set L_inner to zero, copying domains

        variables = self._get_standard_thickness_variables(L_inner, L_outer)

        return variables

    def get_coupled_variables(self, variables):
        param = self.param
        # delta_phi = phi_s - phi_e
        if self.reaction_loc == "interface":
            delta_phi = variables[
                "Lithium metal interface surface potential difference"
            ]
            phi_s_n = variables["Lithium metal interface electrode potential"]
        else:
            delta_phi = variables["Negative electrode surface potential difference"]
            phi_s_n = variables["Negative electrode potential"]

        # Look for current that contributes to the -IR drop
        # If we can't find the interfacial current density from the main reaction, j,
        # it's ok to fall back on the total interfacial current density, j_tot
        # This should only happen when the interface submodel is "InverseButlerVolmer"
        # in which case j = j_tot (uniform) anyway
        if "Negative electrode interfacial current density" in variables:
            j = variables["Negative electrode interfacial current density"]
        elif self.reaction_loc == "interface":
            j = variables["Lithium metal total interfacial current density"]
        else:
            j = variables[
                "X-averaged "
                + self.domain.lower()
                + " electrode total interfacial current density"
            ]

        L_sei_inner = variables[f"Inner {self.reaction} thickness"]
        L_sei_outer = variables[f"Outer {self.reaction} thickness"]
        L_sei = variables[f"Total {self.reaction} thickness"]

        T = variables["Negative electrode temperature"]
        R_sei = param.R_sei
        eta_SEI = delta_phi - j * L_sei * R_sei
        # Thermal prefactor for reaction, interstitial and EC models
        prefactor = 1 / (1 + param.Theta * T)

        if self.options["SEI"] == "reaction limited":
            C_sei = param.C_sei_reaction
            j_sei = -(1 / C_sei) * pybamm.exp(-0.5 * prefactor * eta_SEI)

        elif self.options["SEI"] == "electron-migration limited":
            U_inner = param.U_inner_electron
            C_sei = param.C_sei_electron
            j_sei = (phi_s_n - U_inner) / (C_sei * L_sei_inner)

        elif self.options["SEI"] == "interstitial-diffusion limited":
            C_sei = param.C_sei_inter
            j_sei = -pybamm.exp(-prefactor * delta_phi) / (C_sei * L_sei_inner)

        elif self.options["SEI"] == "solvent-diffusion limited":
            C_sei = param.C_sei_solvent
            j_sei = -1 / (C_sei * L_sei_outer)

        elif self.options["SEI"] == "ec reaction limited":
            C_sei_ec = param.C_sei_ec
            C_ec = param.C_ec

            # we have a linear system for j_sei and c_ec
            #  c_ec = 1 + j_sei * L_sei * C_ec
            #  j_sei = - C_sei_ec * c_ec * exp()
            # so
            #  j_sei = - C_sei_ec * exp() - j_sei * L_sei * C_ec * C_sei_ec * exp()
            # so
            #  j_sei = -C_sei_ec * exp() / (1 + L_sei * C_ec * C_sei_ec * exp())
            #  c_ec = 1 / (1 + L_sei * C_ec * C_sei_ec * exp())
            C_sei_exp = C_sei_ec * pybamm.exp(-0.5 * prefactor * eta_SEI)
            j_sei = -C_sei_exp / (1 + L_sei * C_ec * C_sei_exp)
            c_ec = 1 / (1 + L_sei * C_ec * C_sei_exp)

            # Get variables related to the concentration
            c_ec_av = pybamm.x_average(c_ec)
            c_ec_scale = param.c_ec_0_dim

            if self.reaction == "SEI on cracks":
                variables.update(
                    {
                        "EC concentration on cracks": c_ec,
                        "EC concentration on cracks [mol.m-3]": c_ec * c_ec_scale,
                        "X-averaged EC concentration on cracks": c_ec_av,
                        "X-averaged EC concentration on cracks [mol.m-3]": c_ec_av
                        * c_ec_scale,
                    }
                )
            else:
                variables.update(
                    {
                        "EC surface concentration": c_ec,
                        "EC surface concentration [mol.m-3]": c_ec * c_ec_scale,
                        "X-averaged EC surface concentration": c_ec_av,
                        "X-averaged EC surface concentration [mol.m-3]": c_ec_av
                        * c_ec_scale,
                    }
                )

        if self.options["SEI"] == "ec reaction limited":
            inner_sei_proportion = 0
        else:
            inner_sei_proportion = param.inner_sei_proportion

        # All SEI growth mechanisms assumed to have Arrhenius dependence
        Arrhenius = pybamm.exp(param.E_over_RT_sei * (1 - prefactor))

        j_inner = inner_sei_proportion * Arrhenius * j_sei
        j_outer = (1 - inner_sei_proportion) * Arrhenius * j_sei

        variables.update(self._get_standard_concentration_variables(variables))
        variables.update(self._get_standard_reaction_variables(j_inner, j_outer))

        # Update whole cell variables, which also updates the "sum of" variables
        variables.update(super().get_coupled_variables(variables))

        return variables

    def set_rhs(self, variables):
        if self.reaction_loc == "x-average":
            L_inner = variables[f"X-averaged inner {self.reaction} thickness"]
            L_outer = variables[f"X-averaged outer {self.reaction} thickness"]
            j_inner = variables[
                f"X-averaged inner {self.reaction} interfacial current density"
            ]
            j_outer = variables[
                f"X-averaged outer {self.reaction} interfacial current density"
            ]
            # Note a is dimensionless (has a constant value of 1 if the surface
            # area does not change)
            a = variables["X-averaged negative electrode surface area to volume ratio"]
        else:
            L_inner = variables[f"Inner {self.reaction} thickness"]
            L_outer = variables[f"Outer {self.reaction} thickness"]
            j_inner = variables[f"Inner {self.reaction} interfacial current density"]
            j_outer = variables[f"Outer {self.reaction} interfacial current density"]
            if self.reaction_loc == "interface":
                a = 1
            else:
                a = variables["Negative electrode surface area to volume ratio"]

        # The spreading term acts to spread out SEI along the cracks as they grow.
        # For SEI on initial surface (as opposed to cracks), it is zero.
        if self.reaction == "SEI on cracks":
            if self.reaction_loc == "x-average":
                l_cr = variables["X-averaged negative particle crack length"]
                dl_cr = variables["X-averaged negative particle cracking rate"]
            else:
                l_cr = variables["Negative particle crack length"]
                dl_cr = variables["Negative particle cracking rate"]
            spreading_outer = dl_cr / l_cr * (self.param.L_outer_0 / 10000 - L_outer)
            spreading_inner = dl_cr / l_cr * (self.param.L_inner_0 / 10000 - L_inner)
        else:
            spreading_outer = 0
            spreading_inner = 0

        Gamma_SEI = self.param.Gamma_SEI

        if self.options["SEI"] == "ec reaction limited":
            self.rhs = {L_outer: -Gamma_SEI * a * j_outer + spreading_outer}
        else:
            v_bar = self.param.v_bar
            self.rhs = {
                L_inner: -Gamma_SEI * a * j_inner + spreading_inner,
                L_outer: -v_bar * Gamma_SEI * a * j_outer + spreading_outer,
            }

    def set_initial_conditions(self, variables):
        if self.reaction_loc == "x-average":
            L_inner = variables[f"X-averaged inner {self.reaction} thickness"]
            L_outer = variables[f"X-averaged outer {self.reaction} thickness"]
        else:
            L_inner = variables[f"Inner {self.reaction} thickness"]
            L_outer = variables[f"Outer {self.reaction} thickness"]

        L_inner_0 = self.param.L_inner_0
        L_outer_0 = self.param.L_outer_0

        if self.reaction == "SEI on cracks":
            # Dividing by 10000 makes initial condition effectively zero
            # without triggering division by zero errors
            L_inner_0 = L_inner_0 / 10000
            L_outer_0 = L_outer_0 / 10000
        if self.options["SEI"] == "ec reaction limited":
            self.initial_conditions = {L_outer: L_inner_0 + L_outer_0}
        else:
            self.initial_conditions = {L_inner: L_inner_0, L_outer: L_outer_0}
