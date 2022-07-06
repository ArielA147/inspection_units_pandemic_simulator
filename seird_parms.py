# library imports

# project imports


class SEIRDparameter:
    """
    Hold the parameters values of the SEIRD model
    """
    beta = 0.0145
    phi = 1 / 0.4762
    gamma = 1 / 0.2350
    psi = 0.0028
    i_mask_reduction = 0.5
    s_mask_reduction = 0.1
    si_mask_reduction = 0.75
