import numpy as np

def power_iteration(A, num_iters=100):
    n = A.shape[0]
    b = np.random.rand(n)
    b /= np.linalg.norm(b)

    for _ in range(num_iters):
        b = A @ b
        norm = np.linalg.norm(b)
        if norm == 0:
            break
        b = b / norm

    eigenvalue = b.T @ A @ b
    return eigenvalue, b

def svd(A, k):
    A = np.array(A, dtype=float)

    ATA = A.T @ A
    eigenvalues = []
    eigenvectors = []

    A_copy = ATA.copy()
    for _ in range(k):
        eigval, eigvec = power_iteration(A_copy)
        eigenvalues.append(eigval)
        eigenvectors.append(eigvec)
        A_copy = A_copy - eigval * np.outer(eigvec, eigvec)

    #sorting    
    eigenvalues = np.array(eigenvalues)
    eigenvectors = np.column_stack(eigenvectors)

    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    V = eigenvectors 
    S = np.diag(np.sqrt(eigenvalues)) 
    
    eps = 1e-10
    S_inv = np.diag(1 / (np.sqrt(eigenvalues) + eps))
    U = A @ V @ S_inv

    return U, S, V.T

