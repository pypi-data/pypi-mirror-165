#                           caltransfer methods
# by: Valeria Fonseca Diaz
#  ------------------------------------------------------------------------


import numpy as np
import scipy as sp
from sklearn.cross_decomposition import PLSRegression
from sklearn.linear_model import LinearRegression
from .utils import convex_relaxation
from scipy.spatial.distance import cdist
from scipy.sparse.linalg import svds


def ds_pc_transfer_fit(X_primary, X_secondary, max_ncp):


    '''
    Direct Standardization (DS) based on PCR. Normally calculated with a high number of components (full rank)
    Method based on standard samples

    Parameters
    ----------
    X_primary : ndarray
        A 2-D array corresponding to the spectral matrix. Shape (N, K) from primary domain

    X_secondary : ndarray
        A 2-D array corresponding to the spectral matrix. Shape (N, K) from secondary domain. X_secondary is expected to be paired with X_primary (standard samples)

    max_ncp : int
        Number of pc's to train DS model. For classical DS, max_ncp = K

    Returns
    -------
    out : tuple
        (F,a), where `F` is the standardization matrix and `a` is the offset.
        F : ndarray (K,K)
        a : ndarray (1,K)

    Notes
    -----
    `F` and `a` used as:
        .. math:: X_p = X_s F + a
    If used for a bilinear model of the type
        .. math:: y = X_p B_p + \beta_p
    then the final regression model after DS transfer becomes
        .. math:: B_s = F B_p
        .. math:: \beta_s = a B_p + \beta_p

    References
    ----------
    Y. Wang, D. J. Veltkamp, and B. R. Kowalski, “Multivariate Instrument Standardization,” Anal. Chem., vol. 63, no. 23, pp. 2750–2756, 1991, doi: 10.1021/ac00023a016.

    Examples
    --------

    >>> import numpy as np
    >>> from sklearn.cross_decomposition import PLSRegression
    >>> import pycaltransfer.caltransfer as caltransfer
    >>> F_sim = np.array([[0., -0.2, 1.], [1.,0.6,0.8], [0.4,2.5,-1.3]])
    >>> a_sim = np.array([[2.,5.,4.]])
    >>> X_secondary = np.array([[0., 0., 1.], [1.,0.,0.], [2.,2.,2.], [2.,5.,4.]])
    >>> x_error = np.array([[-0.03774524, -0.00475627,  0.01938877],
    ...       [-0.02925257,  0.1500586 ,  0.01706783],
    ...       [-0.11049506, -0.03469373, -0.03136003],
    ...       [-0.00685062, -0.00367186, -0.07211823]])
    >>> X_primary = X_secondary.dot(F_sim) + a_sim + x_error
    >>> x_mean = np.mean(X_primary, axis = 0)
    >>> x_mean.shape = (1,X_primary.shape[1])
    >>> Y = np.array([[0.1], [0.9], [6.2], [11.9]])
    >>> # plsr model primary domain
    >>> pls2 = PLSRegression(n_components=2,scale=False)
    >>> pls2.fit(X_primary, Y)
    >>> B_p = pls2.coef_
    >>> beta_p = pls2.y_mean_ - (x_mean.dot(B_p)) # baseline model y = X_primary B_p + beta_p
    >>> # DS transfer
    >>> F, a = caltransfer.ds_pc_transfer_fit(X_primary, X_secondary, max_ncp = 2) # with 3 components it's already a perfect fit (possibly over fit)
    >>> B_ds = F.dot(B_p)
    >>> beta_s = a.dot(B_p) + beta_p # transferred model y = X_secondary B_s + beta_s
    >>> print(pls2.predict(X_primary))
    >>> print(pls2.predict(X_secondary.dot(F) + a))
    [[ 0.10057381]
     [ 1.03398846]
     [ 5.95594099]
     [12.00949675]]
    [[ 0.18648704]
     [ 0.80221134]
     [ 6.23273672]
     [11.87856491]]






    '''

    kk = X_primary.shape[1]
    N = X_primary.shape[0]
    ww = 2*kk


    F = np.zeros((kk,kk))
    a = np.zeros((1,kk))

    mean_primary = X_primary.mean(axis=0)
    mean_secondary = X_secondary.mean(axis=0)
    X_primary_c = X_primary - mean_primary
    X_secondary_c = X_secondary - mean_secondary


    X_in = X_secondary_c[:, :]
    current_ncp = np.amin([max_ncp,X_in.shape[1]])


    # ------ svd

    U0,S,V0t = np.linalg.svd(X_in.T.dot(X_in),full_matrices=True)
    S_matrix = np.zeros((current_ncp,current_ncp))
    S_matrix[0:current_ncp,:][:,0:current_ncp] = np.diag(S[0:current_ncp])
    V = V0t[0:current_ncp,:].T
    U = U0[:,0:current_ncp]

    X_out = X_primary_c[:, :]

    F = U.dot(np.linalg.inv(S_matrix)).dot(V.T).dot(X_in.T).dot(X_out)

    a = mean_primary - F.T.dot(mean_secondary)

    a.shape = (1,a.shape[0]) # row vector



    return (F,a)




def pds_pls_transfer_fit(X_primary, X_secondary, max_ncp, ww):

    '''

    (Piecewise) Direct Standardization (PDS) based on PLSR
    Method based on standard samples

    Parameters
    ----------
    X_primary : ndarray
        A 2-D array corresponding to the spectral matrix. Shape (N, K) from primary domain

    X_secondary : ndarray
        A 2-D array corresponding to the spectral matrix. Shape (N, K) from secondary domain. X_secondary is expected to be paired with X_primary (standard samples)

    max_ncp : int
        Number of latent variables for PLSR models.

    ww : int
        Half of the total window width. The total window width is 2*ww + 1

    Returns
    -------
    out : tuple
        (F,a), where `F` is the standardization matrix and `a` is the offset.
        F : ndarray (K,K)
        a : ndarray (1,K)

    Notes
    -----
    `F` and `a` used as:
        .. math:: X_p = X_s F + a
    If used for a bilinear model of the type
        .. math:: y = X_p B_p + \beta_p
    then the final regression model after PDS transfer becomes
        .. math:: B_s = F B_p
        .. math:: \beta_s = a B_p + \beta_p

    References
    ----------
    E. Bouveresse and D. L. Massart, “Improvement of the piecewise direct standardisation procedure for the transfer of NIR spectra for multivariate calibration,”   Chemom. Intell. Lab. Syst., vol. 32, no. 2, pp. 201–213, 1996, doi: 10.1016/0169-7439(95)00074-7.

    Examples
    --------

    >>> import numpy as np
    >>> from sklearn.cross_decomposition import PLSRegression
    >>> import pycaltransfer.caltransfer as caltransfer
    >>> F_sim = np.array([[0., -0.2, 1.], [1.,0.6,0.8], [0.4,2.5,-1.3]])
    >>> a_sim = np.array([[2.,5.,4.]])
    >>> X_secondary = np.array([[0., 0., 1.], [1.,0.,0.], [2.,2.,2.], [2.,5.,4.]])
    >>> x_error = np.array([[-0.03774524, -0.00475627,  0.01938877],
    ...       [-0.02925257,  0.1500586 ,  0.01706783],
    ...       [-0.11049506, -0.03469373, -0.03136003],
    ...       [-0.00685062, -0.00367186, -0.07211823]])
    >>> X_primary = X_secondary.dot(F_sim) + a_sim + x_error
    >>> x_mean = np.mean(X_primary, axis = 0)
    >>> x_mean.shape = (1,X_primary.shape[1])
    >>> Y = np.array([[0.1], [0.9], [6.2], [11.9]])
    >>> # plsr model primary domain
    >>> pls2 = PLSRegression(n_components=2,scale=False)
    >>> pls2.fit(X_primary, Y)
    >>> B_p = pls2.coef_
    >>> beta_p = pls2.y_mean_ - (pls2.x_mean_.dot(B_p)) # baseline model y = X_primary B_p + beta_p
    >>> # PDS transfer
    >>> F, a = caltransfer.pds_pls_transfer_fit(X_primary, X_secondary, max_ncp = 1, ww = 1) # ww = 1 means a total window width of 3
    >>> B_ds = F.dot(B_p)
    >>> beta_s = a.dot(B_p) + beta_p # transferred model y = X_secondary B_s + beta_s
    >>> print(pls2.predict(X_primary))
    >>> print(X_primary.dot(B_p) + beta_p)
    >>> print(pls2.predict(X_secondary.dot(F) + a))
    [[ 0.10057381]
     [ 1.03398846]
     [ 5.95594099]
     [12.00949675]]
    [[ 0.10057381]
     [ 1.03398846]
     [ 5.95594099]
     [12.00949675]]
    [[ 0.76356358]
     [ 0.5984284 ]
     [ 5.69538785]
     [12.04262017]]




    '''

    kk = X_primary.shape[1]
    N = X_primary.shape[0]



    F = np.zeros((kk,kk))
    a = np.zeros((1,kk))

    mean_primary = X_primary.mean(axis=0)
    mean_secondary = X_secondary.mean(axis=0)
    X_primary_c = X_primary - mean_primary
    X_secondary_c = X_secondary - mean_secondary

    for jj_out in range(0,kk):

        # --- wv to predict


        X_out = X_primary_c[:, jj_out]


        # --- input matrix

        ll = np.amax([0, jj_out - ww])
        ul = np.amin([jj_out + ww, kk-1])
        jj_in = np.arange(ll, ul+1)
        X_in = X_secondary_c[:, jj_in]

        chosen_lv = np.amin([max_ncp,X_in.shape[1]])

        # --- pls transfer


        my_pls = PLSRegression(n_components = chosen_lv,scale=False)
        my_pls.fit(X_in, X_out)


        F[jj_in,jj_out] = my_pls.coef_[:,0]


    a[0,:] = mean_primary - F.T.dot(mean_secondary)

    return (F,a)


def epo_fit(X_primary, X_secondary,epo_ncp=1):


    '''

    External Parameter Orthogonalization (EPO) based on spectral value decomposition (SVD) of the difference matrix
    Method based on standard samples

    Parameters
    ----------
    X_primary : ndarray
        A 2-D array corresponding to the spectral matrix. Shape (N, K) from primary domain

    X_secondary : ndarray
        A 2-D array corresponding to the spectral matrix. Shape (N, K) from secondary domain. X_secondary is expected to be paired with X_primary (standard samples)

    epo_ncp : int
        Number of EPO components to remove.

    Returns
    -------
    out : tuple
        (E,a), where `E` is the orthogonalization matrix and `a` is the offset.
        E : ndarray (K,K)
        a : ndarray (1,K)

    Notes
    -----
    `E` comes from `SVD(D)` where `D = X_primary - X_secondary`
    Orthogonalization of matrices as:
        .. math:: X_{pE} = X_p E
        .. math:: X_{sE} = X_s E
    If used for a bilinear model, retrain model using `X_{pE}` and `y`. Obtain model
        .. math:: y = X_{pE} B_e + \beta_e
    No further orthogonalization is needed for future predictions.


    References
    ----------

    M. Zeaiter, J. M. Roger, and V. Bellon-Maurel, “Dynamic orthogonal projection. A new method to maintain the on-line robustness of multivariate calibrations. Application to NIR-based monitoring of wine fermentations,” Chemom. Intell. Lab. Syst., vol. 80, no. 2, pp. 227–235, 2006, doi: 10.1016/j.chemolab.2005.06.011.
    J. M. Roger, F. Chauchard, and V. Bellon-Maurel, “EPO-PLS external parameter orthogonalisation of PLS application to temperature-independent measurement of sugar content of intact fruits,” Chemom. Intell. Lab. Syst., vol. 66, no. 2, pp. 191–204, 2003, doi: 10.1016/S0169-7439(03)00051-0.

    Examples
    --------
    >>> import numpy as np
    >>> import pycaltransfer.caltransfer as caltransfer
    >>> from sklearn.cross_decomposition import PLSRegression
    >>> X_primary = np.array([[0., 0., 1.], [1.,0.,0.], [2.,2.,2.], [2.,5.,4.]])
    >>> x_error = np.array([[-0.03774524, -0.00475627,  0.01938877],
    ...       [-0.02925257,  0.1500586 ,  0.01706783],
    ...       [-0.11049506, -0.03469373, -0.03136003],
    ...       [-0.00685062, -0.00367186, -0.07211823]])
    >>> X_secondary = X_primary + x_error
    >>> # Fit EPO
    >>> E,a = caltransfer.epo_fit(X_primary, X_secondary,epo_ncp=1)
    >>> X_primary_e = X_primary.dot(E) + a
    >>> x_mean_e = np.mean(X_primary_e, axis = 0)
    >>> x_mean_e.shape = (1,X_primary_e.shape[1])
    >>> Y = np.array([[0.1], [0.9], [6.2], [11.9]])
    >>> # PLSR after EPO
    >>> pls2 = PLSRegression(n_components=2,scale=False)
    >>> pls2.fit(X_primary_e, Y)
    >>> B_pe = pls2.coef_
    >>> beta_pe = pls2.y_mean_ - (x_mean_e.dot(B_pe)) # Model after EPO y = X_se B_pe + beta_pe; X_se = X_s E +a
    >>> B_s = B_pe
    >>> beta_s = beta_pe
    >>> print(X_secondary.dot(B_s) + beta_s)
    >>> print(Y)
    [[ 0.47210387]
     [-0.01622479]
     [ 6.95309782]
     [10.92865516]]
    [[ 0.1]
     [ 0.9]
     [ 6.2]
     [11.9]]


    '''

    D = X_primary - X_secondary


    U0,S,V0t = np.linalg.svd(D)
    S_matrix = np.zeros((epo_ncp,epo_ncp))
    S_matrix[0:epo_ncp,:][:,0:epo_ncp] = np.diag(S[0:epo_ncp])
    V = V0t[0:epo_ncp].T
    U = U0[:,0:epo_ncp]

    E = np.identity(n=V.shape[0]) - V.dot(V.T)
    a = np.mean(X_primary,axis=0)
    a.shape = (1,a.shape[0]) # row vector


    return (E, a)


def jointypls_regression(tscores_primary,tscores_secondary, y_primary, y_secondary):

    '''

    Re-specification of Q parameters based on scores variables (or latent variables) from an existing PLSR model.
    This function should be used for univariate response (y 1D)

    Parameters
    ----------
    tscores_primary : ndarray
        A 2-D array containing the scores of the primary domain spectra (assumed to be centered). Shape (Np,A)

    tscores_secondary : ndarray
        A 2-D array containing the scores of the secondary domain spectra (assumed to be centered). Shape (Ns,A)

    y_primary : ndarray
         A 1-D array with reference values of primary spectra. Shape (Np,)

    y_secondary : ndarray
        A 1-D array with reference values of secondary spectra. Shape (Ns,)

    Returns
    -------
    out : tuple
        (q_jpls,b), where `q_jpls` is the set of coefficients in the output layer of the bilinear model and `b` is the new intercept.
        q_jpls : array of shape (A,)
        a : float

    Notes
    -----
    If used for a bilinear model of the type
        .. math:: y = X_p B_p + \beta_p
    where `B_p = Rq`, then the new regression vector is
        .. math:: B_{jpls} = Rq_{jpls}
        .. math:: \beta_{jpls} = b - (\bar(x) B_{jpls})

    References
    ----------
    S. García Muñoz, J. F. MacGregor, and T. Kourti, “Product transfer between sites using Joint-Y PLS,” Chemom. Intell. Lab. Syst., vol. 79, no. 1–2, pp. 101–114, 2005, doi: 10.1016/j.chemolab.2005.04.009.
    A. Folch-Fortuny, R. Vitale, O. E. de Noord, and A. Ferrer, “Calibration transfer between NIR spectrometers: New proposals and a comparative study,” J. Chemom., vol. 31, no. 3, pp. 1–11, 2017, doi: 10.1002/cem.2874.

    Examples
    --------

    >>> import numpy as np
    >>> from sklearn.cross_decomposition import PLSRegression
    >>> import pycaltransfer.caltransfer as caltransfer
    >>> X_secondary = np.array([[0., 0., 1.], [1.,0.,0.], [2.,2.,2.], [2.,5.,4.]])
    >>> x_error = np.array([[-0.03774524, -0.00475627,  0.01938877],
    ...       [-0.02925257,  0.1500586 ,  0.01706783],
    ...       [-0.11049506, -0.03469373, -0.03136003],
    ...       [-0.00685062, -0.00367186, -0.07211823]])
    >>> X_primary = X_secondary + x_error
    >>> x_mean = np.mean(X_primary, axis = 0)
    >>> x_mean.shape = (1,X_primary.shape[1])
    >>> Y = np.array([[0.1], [0.9], [6.2], [11.9]])
    >>> # PLSR
    >>> pls2 = PLSRegression(n_components=2,scale=False)
    >>> pls2.fit(X_primary, Y)
    >>> R_p = pls2.x_rotations_
    >>> B_p = pls2.coef_
    >>> beta_p = pls2.y_mean_ - (x_mean.dot(B_p)) # baseline model y = X_primary B_p + beta_p
    >>> # Transfer with Joint Y PLS. Here a subset of samples or other samples can be used. For the example we use the same samples
    >>> tprimary = (X_primary-x_mean).dot(R_p)
    >>> tsecondary = (X_secondary-x_mean).dot(R_p)
    >>> y_primary = Y[:,0] # flatten 1D
    >>> y_secondary = Y[:,0] # flatten 1D
    >>> q_jpls,b_jpls = caltransfer.jointypls_regression(tprimary, tsecondary, y_primary, y_secondary)
    >>> B_jpls = R_p.dot(q_jpls)
    >>> beta_jpls = np.asarray(b_jpls - (x_mean).dot(B_jpls))
    >>> print(X_primary.dot(B_jpls) + beta_jpls)
    >>> print(X_secondary.dot(B_jpls) + beta_jpls)
    [ 0.0759273   1.01125531  6.07352354 11.87814864]
    [ 0.12036472  0.81699714  6.28765203 11.93613132]


    '''

    t_jointpls = np.concatenate((tscores_primary,tscores_secondary), axis = 0)
    y_jointpls = np.concatenate((y_primary,y_secondary), axis = 0)


    calmodel_tr_jointpls = LinearRegression()
    calmodel_tr_jointpls.fit(t_jointpls,y_jointpls) # output values need to be 1D always here

            # output

    q_jpls = calmodel_tr_jointpls.coef_
    b_jpls = calmodel_tr_jointpls.intercept_


    return (q_jpls,b_jpls)



def slope_bias_correction(y_secondary, y_secondary_pred):

    '''

    Slope and Bias Correction (SBC) as `y_secondary = b + s*y_secondary_pred`
    This function should be used for univariate response (y 1D)

    Parameters
    ----------
    y_secondary : ndarray
        A 1-D array with observed reference values of secondary spectra. Shape (Ns,)

    y_secondary_pred : ndarray
        A 1-D array with predicted reference values of secondary spectra using primary model. Shape (Ns,)

    Returns
    -------
    out : tuple
        (slope,bias)
        slope : float
        bias : float

    Notes
    -----

    SBC corrects the predictions as `y = y_pred *s + b`
    If used for a bilinear model of the type
        .. math:: y = X_p B_p + \beta_p
    then the transferred model becomes
        .. math:: B_s = B_p*s
        .. math:: \beta_s = \beta_p*s + b

    References
    ----------
    T. Fearn, “Standardisation and calibration transfer for near infrared instruments: A review,” J. Near Infrared Spectrosc., vol. 9, no. 4, pp. 229–244, 2001, doi: 10.1255/jnirs.309.

    Examples
    --------
    >>> import numpy as np
    >>> from sklearn.cross_decomposition import PLSRegression
    >>> import pycaltransfer.caltransfer as caltransfer
    >>> X_secondary = np.array([[0., 0., 1.], [1.,0.,0.], [2.,2.,2.], [2.,5.,4.]])
    >>> x_error = np.array([[-0.03774524, -0.00475627,  0.01938877],
    ...       [-0.02925257,  0.1500586 ,  0.01706783],
    ...       [-0.11049506, -0.03469373, -0.03136003],
    ...       [-0.00685062, -0.00367186, -0.07211823]])
    >>> X_primary = X_secondary + x_error
    >>> x_mean = np.mean(X_primary, axis = 0)
    >>> x_mean.shape = (1,X_primary.shape[1])
    >>> Y = np.array([[0.1], [0.9], [6.2], [11.9]])
    >>> # PLSR
    >>> pls2 = PLSRegression(n_components=2,scale=False)
    >>> pls2.fit(X_primary, Y)
    >>> R_p = pls2.x_rotations_
    >>> B_p = pls2.coef_
    >>> beta_p = pls2.y_mean_ - (x_mean.dot(B_p)) # baseline model y = X_primary B_p + beta_p
    >>> # Transfer with Slope and Bias Correction
    >>> y_secondary = Y[:,0]
    >>> y_secondary_pred = X_secondary.dot(B_p) + beta_p
    >>> slope, bias = caltransfer.slope_bias_correction(y_secondary, y_secondary_pred)
    >>> B_sbc = B_p.dot(slope)
    >>> beta_sbc = beta_p.dot(slope) + bias
    >>> print(y_secondary)
    >>> print(X_secondary.dot(B_sbc) + beta_sbc)
    [ 0.1  0.9  6.2 11.9]
    [ 0.15333474  0.81766258  6.25070668 11.87829601]

    '''

    sbc = LinearRegression()
    sbc.fit(y_secondary_pred, y_secondary)

    slope = sbc.coef_
    bias = sbc.intercept_

    return (slope, bias)




def dipals(xcal, ycal, xs, xt, A, l, center_mode = "target", heuristic=False):

        '''
        Domain-invariant partial least squares regression (di-PLS) performs PLS regression
        using labeled Source domain data x (=xs) and y and unlabeled Target domain data (xt)
        with the goal to fit an (invariant) model that generalizes over both domains.



        Parameters
        ----------
        xcal: numpy array (N,K)
            Labeled X data

        ycal: numpy array (N,1)
            Response variable

        xs: numpy array (N_S,K)
            Source domain data

        xt: numpy array (N_T, K)
            Target domain data.

        A: int
            Number of latent variables

        l: int or numpy array (A x 1)
            Regularization parameter: Typically 0 < l < 1e10
            If Array is passed, a different l is used for each LV

        center_mode: str, default "target"
            "calibration" (x), "source" (xs) or "target" (xt). This is the mode to recenter the matrices for final prediction.

        heuristic: str
            If 'True' the regularization parameter is determined using a
            heuristic that gives equal weight to:
            i) Fitting the output variable y and
            ii) Minimizing domain discrepancy.
            For details see ref. (3).


        Returns
        -------
        B: numpy array (K,1)
            Regression vector

        beta: float
            Offset (See Notes)

        T: numpy array (N,A)
            Training data projections (scores)

        Ts: numpy array (N_S,A)
            Source domain projections (scores)

        Tt: numpy array (N_T,A)
            Target domain projections (scores)

        W: numpy array (K,A)
            Weight vector

        P: numpy array (K,A)
            Loadings vector

        E: numpy array (N_S,K)
            Residuals of labeled X data

        Es: numpy array (N_S,K)
            Source domain residual matrix

        Et: numpy array (N_T,K)
            Target domain residual matrix

        Ey: numpy array (N_S,1)
            Response variable residuals

        C: numpy array (A,1)
            Regression vector, such that
            y = Ts*C

        opt_l: numpy array (A,1)
            The heuristically determined regularization parameter for each LV
            (if heuristic = 'True')

        discrepancy: numpy array (A,)
            Absolute difference between variance of source and target domain projections


        Notes
        -----
        For this bilinear model, the final model for target  (secondary) data is specified as

            .. math:: \beta = b_0 - (\hat(x)B)
            .. math:: y = xt B + \beta

        References
        ----------

        (1) Ramin Nikzad-Langerodi, Werner Zellinger, Edwin Lughofer, and Susanne Saminger-Platz
          "Domain-Invariant Partial Least Squares Regression" Analytical Chemistry 2018 90 (11),
          6693-6701 DOI: 10.1021/acs.analchem.8b00498
        (2) Ramin Nikzad-Langerodi, Werner Zellinger, Susanne Saminger-Platz and Bernhard Moser
          "Domain-Invariant Regression under Beer-Lambert's Law" In Proc. International Conference
          on Machine Learning and Applications, Boca Raton FL 2019.
        (3) Ramin Nikzad-Langerodi, Werner Zellinger, Susanne Saminger-Platz, Bernhard A. Moser,
          Domain adaptation for regression under Beer–Lambert’s law, Knowledge-Based Systems,
          2020 (210) DOI: 10.1016/j.knosys.2020.106447

        Examples
        --------

        For a full application see the jupyter notebooks at https://gitlab.com/vfonsecad/pycaltransfer



        '''

        # Get array dimensions
        (n, k) = np.shape(xcal)
        (ns, k) = np.shape(xs)
        (nt, k) = np.shape(xt)


        # Center all matrices
        b0 = np.mean(ycal,axis=0)
        x_mu = np.mean(xcal, 0)           # Column means of x
        xs_mu = np.mean(xs, 0)         # Column means of xs
        xt_mu = np.mean(xt, 0)         # Column means of xt


        x = xcal - x_mu
        xs = xs - xs_mu
        xt = xt - xt_mu

        if center_mode == "calibration":

            x_mu_final = x_mu.copy()

        elif center_mode == "source":

            x_mu_final = xs_mu.copy()

        elif center_mode == "target":

            x_mu_final = xt_mu.copy()

        y = ycal.copy()

        if y.ndim == 1:
            y.shape = (y.shape[0], 1)




        # Initialize matrices
        T = np.zeros([n, A])
        P = np.zeros([k, A])

        Tt = np.zeros([nt, A])
        Pt = np.zeros([k, A])

        Ts = np.zeros([ns, A])
        Ps = np.zeros([k, A])

        W = np.zeros([k, A])
        C = np.zeros([A, 1])
        opt_l = np.zeros(A)
        discrepancy = np.zeros(A)

        I = np.eye(k)

        l = np.asarray(l).flatten()

        # Compute LVs
        for i in range(A):


            if l.shape[0]>1:

                lA = l[i]

            else:

                lA = l[0]


            # Compute Domain-Invariant Weight Vector
            w_pls = ((y.T@x)/(y.T@y))  # Ordinary PLS solution



            # Convex relaxation of covariance difference matrix
            D = convex_relaxation(xs, xt)

            if(heuristic is True): # Regularization parameter heuristic

                w_pls = w_pls/np.linalg.norm(w_pls)
                gamma = (np.linalg.norm((x-y@w_pls))**2)/(w_pls@D@w_pls.T)
                opt_l[i] = gamma
                lA = gamma


            # Compute di-PLS weight vector
            # reg = (np.linalg.inv(I+lA/((y.T@y))*D))
            # w = w_pls@reg
            reg = I+lA/((y.T@y))*D
            w = sp.linalg.solve(reg.T, w_pls.T, assume_a='sym').T  # ~10 times faster

            # Normalize w
            w = w/np.linalg.norm(w)


            # Absolute difference between variance of source and target domain projections
            discrepancy[i] = w@D@w.T


            # Compute scores
            t = x@w.T
            ts = xs@w.T
            tt = xt@w.T

            # Regress y on t
            c = (y.T@t)/(t.T@t)

            # Compute loadings
            p = (t.T@x)/(t.T@t)
            ps = (ts.T@xs)/(ts.T@ts)
            pt = (tt.T@xt)/(tt.T@tt)

            # Deflate X and y (Gram-Schmidt orthogonalization)

            t.shape = (t.shape[0],1)
            ts.shape = (ts.shape[0],1)
            tt.shape = (tt.shape[0],1)




            x = x - t@p
            xs = xs - ts@ps
            xt = xt - tt@pt
            y = y - t*c

            # Store w,t,p,c
            W[:, i] = w
            T[:, i] = t.reshape(n)
            Ts[:, i] = ts.reshape(ns)
            Tt[:, i] = tt.reshape(nt)
            P[:, i] = p.reshape(k)
            Ps[:, i] = ps.reshape(k)
            Pt[:, i] = pt.reshape(k)
            C[i] = c


        # Calculate regression vector
        B = W@(np.linalg.inv(P.T@W))@C

        # Store residuals
        E = x
        Es = xs
        Et = xt
        Ey = y

        #Offset

        beta = b0 - (x_mu_final@B)

        return B, beta, T, Ts, Tt, W, P, Ps, Pt, E, Es, Et, Ey, C, opt_l, discrepancy



def sst(X_primary, X_secondary, ncomp):


    '''
    Spectral Space Transformation (SST).
    Method based on standard samples

    Parameters
    ----------
    X_primary : ndarray
        A 2-D array corresponding to the spectral matrix. Shape (N, K) from primary domain

    X_secondary : ndarray
        A 2-D array corresponding to the spectral matrix. Shape (N, K) from secondary domain. X_secondary is expected to be paired with X_primary (standard samples)

    ncomp : int
        Number of pc's to perform SVD reduction.

    Returns
    -------
    out : tuple
        (F,a), where `F` is the standardization matrix and `a` is the offset.
        F : ndarray (K,K)
        a : ndarray (1,K)

    Notes
    -----
    `F` and `a` used as:
        .. math:: X_p = X_s F + a
    If used for a bilinear model of the type
        .. math:: y = X_p B_p + \beta_p
    then the final regression model after DS transfer becomes
        .. math:: B_s = F B_p
        .. math:: \beta_s = a B_p + \beta_p

    References
    ----------
    W. Du et al., “Maintaining the predictive abilities of multivariate calibration models by spectral space transformation,” Anal. Chim. Acta, vol. 690, no. 1, pp. 64–70, 2011, doi: 10.1016/j.aca.2011.02.014.

    Examples
    --------

    >>> import numpy as np
    >>> from sklearn.cross_decomposition import PLSRegression
    >>> import pycaltransfer.caltransfer as caltransfer
    >>> F_sim = np.array([[0., -0.2, 1.], [1.,0.6,0.8], [0.4,2.5,-1.3]])
    >>> a_sim = np.array([[2.,5.,4.]])
    >>> X_secondary = np.array([[0., 0., 1.], [1.,0.,0.], [2.,2.,2.], [2.,5.,4.]])
    >>> x_error = np.array([[-0.03774524, -0.00475627,  0.01938877],
    ...       [-0.02925257,  0.1500586 ,  0.01706783],
    ...       [-0.11049506, -0.03469373, -0.03136003],
    ...       [-0.00685062, -0.00367186, -0.07211823]])
    >>> X_primary = X_secondary.dot(F_sim) + a_sim + x_error
    >>> x_mean = np.mean(X_primary, axis = 0)
    >>> x_mean.shape = (1,X_primary.shape[1])
    >>> Y = np.array([[0.1], [0.9], [6.2], [11.9]])
    >>> y_mean = np.mean(Y, axis = 0)
    >>> # plsr model primary domain
    >>> pls2 = PLSRegression(n_components=2,scale=False)
    >>> pls2.fit(X_primary, Y)
    >>> B_p = pls2.coef_
    >>> beta_p = y_mean - (x_mean.dot(B_p)) # baseline model y = X_primary B_p + beta_p
    # SST transfer
    >>> F, a = caltransfer.sst(X_primary, X_secondary, ncomp = 2) # with 3 components it's already a perfect fit (possibly overfit)
    >>> B_ds = F.dot(B_p)
    >>> beta_s = a.dot(B_p) + beta_p # transferred model y = X_secondary B_s + beta_s
    >>> print(pls2.predict(X_primary))
    >>> print(pls2.predict(X_secondary.dot(F) + a))
        [[ 0.10057381]
         [ 1.03398846]
         [ 5.95594099]
         [12.00949675]]
        [[ 0.1351422 ]
         [ 0.71033383]
         [ 6.49088307]
         [11.76364089]]


    '''


    k = X_primary.shape[1]
    X_primary_mean = np.mean(X_primary, axis=0)
    X_secondary_mean = np.mean(X_secondary, axis=0)
    X_primary_mean.shape = (1,X_primary_mean.shape[0])
    X_secondary_mean.shape = (1,X_secondary_mean.shape[0])

    X_primary_c = X_primary - X_primary_mean
    X_secondary_c = X_secondary - X_secondary_mean

    X_comb = np.concatenate((X_primary_c, X_secondary_c), axis = 1)


    U, S, Vt = np.linalg.svd(X_comb)

    U = U[:,0:ncomp]
    S = S[0:ncomp]
    Vt = Vt[0:ncomp,:]
    V = Vt.T

    Vp = V[0:k,:]
    Vs = V[k:,:]


    F = np.eye(k)+np.linalg.pinv(Vs.T).dot(Vp.T - Vs.T)
    a = X_primary_mean - (X_secondary_mean.dot(F))

    return (F,a)



def top(X_tuple,top_ncp=1):


    '''
    Transfer by orthogonal projection (TOP).
    Method proposed for standardization samples and transfer to multiple devices.

    Parameters
    ----------
    X_tuple : tuple of ndarray's
        Each array is a  2-D array corresponding to the spectral matrix. Shape (N, K) for N transfer or standardization samples


    top_ncp : int
        Number of TOP components to remove.

    Returns
    -------
    out : ndarray
        E, where `E` is the orthogonalization matrix.
        E : ndarray (K,K)


    Notes
    -----
    `E` comes from `SVD(R)` where `R` contains in each row the mean of one instrument.
    Orthogonalization of matrices as:
        .. math:: X_{pE} = X_p E
        .. math:: X_{sE} = X_s E
    If used for a bilinear model, retrain model using `X_{pE}` and `y`. Obtain model
        .. math:: y = X_{pE} B_e + \beta_e
    No further orthogonalization is needed for future predictions.


    References
    ----------

     A. Andrew and T. Fearn, “Transfer by orthogonal projection: Making near-infrared calibrations robust to between-instrument variation,” Chemom. Intell. Lab. Syst., vol. 72, no. 1, pp. 51–56, 2004, doi: 10.1016/j.chemolab.2004.02.004.

    Examples
    --------

    >>> import numpy as np
    >>> import pycaltransfer.caltransfer as caltransfer
    >>> from sklearn.cross_decomposition import PLSRegression
    >>> X_primary = np.array([[0., 0., 1.], [1.,0.,0.], [2.,2.,2.], [2.,5.,4.]])
    >>> x_error = np.array([[-0.03774524, -0.00475627,  0.01938877],
    ...       [-0.02925257,  0.1500586 ,  0.01706783],
    ...       [-0.11049506, -0.03469373, -0.03136003],
    ...       [-0.00685062, -0.00367186, -0.07211823]])
    >>> X_secondary = X_primary + x_error
    >>> # TOP
    >>> E = caltransfer.top((X_primary, X_secondary),top_ncp=1)
    >>> X_primary_e = X_primary.dot(E)
    >>> x_mean_e = np.mean(X_primary_e, axis = 0)
    >>> x_mean_e.shape = (1,X_primary_e.shape[1])
    >>> Y = np.array([[0.1], [0.9], [6.2], [11.9]])
    >>> y_mean = np.mean(Y, axis = 0)
    >>> # PLSR after TOP
    >>> pls2 = PLSRegression(n_components=2,scale=False)
    >>> pls2.fit(X_primary_e, Y)
    >>> B_s = pls2.coef_
    >>> beta_s = y_mean - (x_mean_e.dot(B_s)) # Model after TOP y = X_s B_s + beta_s
    >>> print(X_secondary.dot(B_s) + beta_s)
    >>> print(Y)
        [[ 0.38884864]
         [ 3.76654062]
         [ 3.75167162]
         [12.49809575]]
        [[ 0.1]
         [ 0.9]
         [ 6.2]
         [11.9]]




    '''

    m = len(X_tuple)
    k = X_tuple[0].shape[1]

    assert m > top_ncp, "top_ncp must be less than m. m is {:d}".format(m)

    R = np.zeros((m,k))

    for mi in range(m):

        R[mi,:] = X_tuple[mi].mean(axis=0)


    U0,S,V0t = np.linalg.svd(R)
    S_matrix = np.zeros((top_ncp,top_ncp))
    S_matrix[0:top_ncp,:][:,0:top_ncp] = np.diag(S[0:top_ncp])
    V = V0t[0:top_ncp].T
    U = U0[:,0:top_ncp]

    E = np.identity(n=V.shape[0]) - V.dot(V.T)


    return E



def dop(Xsou, Ysou, Xtar, Ytar, rho, dop_ncomp = 3):

    '''
    Dynamic orthogonal projection (DOP) with Gaussian kernel
    Standard-free method based on reference values of a target domain

    Parameters
    ----------
    Xsou: numpy array (N,K)
        Spectral calibration data from source domain

    Ysou: numpy array (N,1)
        Reference values for calibration from source domain

    Xtar: numpy array (N_t,K)
        Spectral data from target domain

    Ytar: numpy array (N_t,1)
        Reference values from target domain

    rho: float
        Precision parameter for Gaussian kernel

    dop_ncomp : int
        Number of DOP components to remove.

    Returns
    -------
    out : ndarray
        E, where `E` is the orthogonalization matrix.
        E : ndarray (K,K)


    Notes
    -----
    `E` comes from `SVD(D)` with `D = Xtar - Xtar_hat` where `Xtar_hat` is the matrix with supervised virtual standard samples
    Orthogonalization of matrices as:
        .. math:: X_{pE} = X_p E
        .. math:: X_{sE} = X_s E
    If used for a bilinear model, retrain model using `X_{pE}` and `y`. Obtain model
        .. math:: y = X_{pE} B_e + \beta_e
    No further orthogonalization is needed for future predictions.


    References
    ----------

    M. Zeaiter, J. M. Roger, and V. Bellon-Maurel, “Dynamic orthogonal projection. A new method to maintain the on-line robustness of multivariate calibrations. Application to NIR-based monitoring of wine fermentations,” Chemom. Intell. Lab. Syst., vol. 80, no. 2, pp. 227–235, 2006, doi: 10.1016/j.chemolab.2005.06.011.


    Examples
    --------

    >>> import numpy as np
    >>> import pycaltransfer.caltransfer as caltransfer
    >>> from sklearn.cross_decomposition import PLSRegression
    >>> Xsou = np.array([[0., 0., 1.], [1.,0.,0.], [2.,2.,2.], [2.,5.,4.]])
    >>> x_error = np.array([[-0.03774524, -0.00475627,  0.01938877],
    ...       [-0.02925257,  0.1500586 ,  0.01706783],
    ...       [-0.11049506, -0.03469373, -0.03136003],
    ...       [-0.00685062, -0.00367186, -0.07211823]])
    >>> Xtar = Xsou + x_error
    >>> Ysou = np.array([[0.1], [0.9], [6.2], [11.9]])
    >>> Ytar = np.array([[0.4], [0.7], [6], [13]])
    >>> # DOP
    >>> E = caltransfer.dop(Xsou, Ysou, Xtar, Ytar, rho = 10, dop_ncomp = 1)
    >>> Xsou_e = Xsou.dot(E)
    >>> x_mean_e = np.mean(Xsou_e, axis = 0)
    >>> x_mean_e.shape = (1,Xsou_e.shape[1])
    >>> y_mean = np.mean(Ysou, axis = 0)
    >>> # PLSR after EPO
    >>> pls2 = PLSRegression(n_components=2,scale=False)
    >>> pls2.fit(Xsou_e, Ysou)
    >>> B_s = pls2.coef_
    >>> beta_s = y_mean - (x_mean_e.dot(B_s)) # Model after TOP y = X_s B_s + beta_s
    >>> print(Xtar.dot(B_s) + beta_s)
    >>> print(Ytar)
        [[ 0.7848724 ]
         [ 0.46202639]
         [ 5.87275856]
         [11.83470517]]
        [[ 0.4]
         [ 0.7]
         [ 6. ]
         [13. ]]


    '''

    Ysouq = Ysou.copy()
    if Ysouq.ndim < 2:
        Ysouq.shape = (Ysou.shape[0],1)

    Ytarq = Ytar.copy()
    if Ytarq.ndim < 2:
        Ytarq.shape = (Ytar.shape[0],1)



    F = np.exp(-rho*cdist(Ytarq, Ysouq, metric='euclidean'))
    denom = F.sum(axis=1)
    denom.shape = (denom.shape[0],1)
    F /= np.tile(denom,(1,F.shape[1]))


    Xtar_hat = F.dot(Xsou)

    E,a = epo_fit(Xtar_hat, Xtar, epo_ncp = dop_ncomp)

    return E


def linear_tca(Xs, Xt, a , mu):

    '''

    Transfer component analysis (TCA) using linear kernel
    Method adapted from Python library `transfertools` by Vincent Vercruyssen (2019)


    Parameters
    ----------

    Xs: numpy array (ns,p)
        Source domain data (non centered)

    Xt: numpy array (nt, p)
        Target domain data (non centered)

    a: int
        Number of latent variables

    mu: float
        Trade-off parameter.


    Returns
    -------
    R: numpy array (p,a)
        Projection loadings

    xs_mean: numpy array (p,)
        mean of source domain

    xt_mean: numpy array (p,)
        mean of target domain

    x_mean: numpy array (p,)
        mean of combined domains


    Notes
    -----
    Source or target matrices are projected as

            .. math:: Ts = Xs R
            .. math:: Tt = Xt R


    Examples
    --------

    >>> from sklearn.linear_model import LinearRegression
    >>> import numpy as np
    >>> import pycaltransfer.caltransfer as caltransfer
    >>> Xs = np.random.multivariate_normal(np.array([0.4, 0.4]), np.diag([0.1,2]), size = 100)
    >>> Xt = np.random.multivariate_normal(-np.array([0.4, 0.4]), np.diag([0.01,2]), size = 500)
    >>> ys = np.random.normal(size = 100)
    >>> R, xs_mean, xt_mean, x_mean = linear_tca(Xs = Xs, Xt = Xt, a = 2, mu = 0.001)
    >>> Ts = (Xs-xs_mean).dot(R)
    >>> lr_tca = LinearRegression()
    >>> lr_tca.fit(Ts,ys)
    >>> # coefficients of lr
    >>> q_tca = lr_tca.coef_
    >>> b_tca = lr_tca.intercept_
    >>> # final bilinear model for target domain
    >>> B_tca = R.dot(q_tca)
    >>> beta_tca = b_tca - xt_mean.dot(B_tca)




    References
    -----------

    Pan, S. J., Tsang, I. W., Kwok, J. T., & Yang, Q. (2010).
        Domain adaptation via transfer component analysis.
        IEEE Transactions on Neural Networks, 22(2), 199-210.


    '''

    ns, p = Xs.shape
    nt, p = Xt.shape


    # linear kernel matrix
    Xst = np.concatenate((Xs, Xt), axis=0)
    K = np.dot(Xst, Xst.T)

    # coefficient matrix L
    L = np.vstack((
        np.hstack((
            np.ones((ns, ns)) / ns ** 2,
            -1.0 * np.ones((ns, nt)) / (ns * nt))),
        np.hstack((
            -1.0 * np.ones((nt, ns)) / (ns * nt),
            np.ones((nt, nt)) / (nt ** 2)))
        ))

    # centering matrix H
    H = np.eye(ns + nt) - np.ones((ns + nt, ns + nt)) / np.float64(ns + nt)

    # matrix Lagrangian objective function: (I + mu*K*L*K)^{-1}*K*H*K
    J = np.dot(np.linalg.inv(np.eye(ns + nt) +
               mu * np.dot(np.dot(K, L), K)),
               np.dot(np.dot(K, H), K))

    # print(J)

    # eigenvector decomposition as solution to trace minimization
    W, _,_ =  svds(J, k = a, which = "LM")   # using svds because eigs was still returning complex-type output


    R = np.dot(Xst.T, W[:,0:a])
    xs_mean = Xs.mean(axis=0)
    xt_mean = Xt.mean(axis=0)
    x_mean = Xst.mean(axis=0)

    return R, xs_mean, xt_mean, x_mean






def Vsou_sign(Vsou, Vtar, V):

    Vsou_sign = np.zeros(Vsou.shape)

    for h in range(Vsou.shape[1]):

        if np.sign(V[:,h].dot(Vsou[:,h])) != np.sign(V[:,h].dot(Vtar[:,h])):

            Vsou_sign[:,h] = -1*Vsou[:,h]

        else:

            Vsou_sign[:,h] = Vsou[:,h]

    return Vsou_sign

def udop(Xsou, Xtar, udop_ncomp = 1, svd_ncomp = 20):


    '''
    Unsupervised dynamic orthogonal projection (uDOP) 
    Standard-free method based on a separate set from a target domain

    Parameters
    ----------
    Xsou: numpy array (N,K)
        Spectral calibration data from source domain


    Xtar: numpy array (N_t,K)
        Spectral data from target domain


    udop_ncomp : int
        Number of DOP components to remove.

    svd_ncomp: int
        Number of components for SVD

    Returns
    -------
    out : ndarray
        E, where `E` is the orthogonalization matrix.
        E : ndarray (K,K)


    Notes
    -----
    `E` comes from `SVD(D)` with `D = Xtar - Xtar_hat` where `Xtar_hat` is the matrix with unsupervised virtual standard samples
    Orthogonalization of matrices as:
        .. math:: X_{pE} = X_p E
        .. math:: X_{sE} = X_s E
    If used for a bilinear model, retrain model using `X_{pE}` and `y`. Obtain model
        .. math:: y = X_{pE} B_e + \beta_e
    No further orthogonalization is needed for future predictions.


    Examples
    --------

    >>> import numpy as np
    >>> import pycaltransfer.caltransfer as caltransfer
    >>> from sklearn.cross_decomposition import PLSRegression
    >>> # Separate sets of spectral measurements
    >>> Xsou = np.array([[0., 0., 1.], [1.,0.,0.], [2.,2.,2.], [2.,5.,4.]])
    >>> Xtar = np.array([[0.1, 0., 1.], [2.5,2.,3], [0.5,1.5,4.]])
    >>> # Reference values for source to orthogonalize model
    >>> Y = np.array([[0.1], [0.9], [6.2], [11.9]])
    >>> # uDOP
    >>> E = caltransfer.udop(Xsou,  Xtar, udop_ncomp = 1, svd_ncomp = 20)
    >>> Xsou_e = Xsou.dot(E) 
    >>> x_mean_e = np.mean(Xsou_e, axis = 0)
    >>> x_mean_e.shape = (1,Xsou_e.shape[1])
    >>> y_mean = np.mean(Y, axis = 0)
    >>> # PLSR after EPO
    >>> pls2 = PLSRegression(n_components=2,scale=False)
    >>> pls2.fit(Xsou_e, Y)
    >>> B = pls2.coef_
    >>> beta = y_mean - (x_mean_e.dot(B)) # Model after TOP y = X_s B_s + beta_s
    >>> print(Xtar.dot(B_s) + beta) # predicted values in target domain
        [[0.23721768]
         [7.42987129]
         [4.62768997]]


    
    References
    ----------
    Valeria Fonseca Diaz, Jean-Michel Roger, Wouter Saeys. Unsupervised dynamic orthogonal projection. An efficient approach to calibration transfer without standard samples. Analytica Chimica Acta. Volume 1225,2022,340154, https://doi.org/10.1016/j.aca.2022.340154.
    
 
    '''

    Xconcat = np.concatenate((Xsou, Xtar), axis = 0)


    Us0, Ss0, Vs_t0 = np.linalg.svd(Xsou - Xsou.mean(axis=0))
    Ut0, St0, Vt_t0 = np.linalg.svd(Xtar - Xtar.mean(axis=0))
    U0, S0, V_t0 = np.linalg.svd(Xconcat - Xconcat.mean(axis=0))




    Vs_t = Vs_t0[0:svd_ncomp,:]
    Vsou = Vs_t.T

    Vt_t = Vt_t0[0:svd_ncomp,:]
    Vtar = Vt_t.T

    V_t = V_t0[0:svd_ncomp,:]
    V = V_t.T



    Vsou_s = Vsou_sign(Vsou, Vtar, V)


    Xtar_hat = (Xtar - Xtar.mean(axis=0)).dot(Vtar).dot(Vsou_s.T) + Xtar.mean(axis=0)


    E,a = epo_fit(Xtar_hat, Xtar, epo_ncp = udop_ncomp)

    return E
