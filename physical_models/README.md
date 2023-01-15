# Models description

1. Rocket railroad car

$$
x = \begin{bmatrix}
    \hat{x}, v
\end{bmatrix}^{T}
$$


$$
\dot{x}(t) = 
\begin{bmatrix} 
    0 & 1 \\ 
    0 & 0 
\end{bmatrix} x(t) + \begin{bmatrix} 
    0 \\ 
    1 
\end{bmatrix} u(t)
$$

2. Seeker

$$
x = 
\begin{bmatrix}
    \hat{x}, \hat{y}, \alpha
\end{bmatrix}^{T}
$$

$$
\dot{x}(t) = 
\begin{bmatrix} 
    v \sin(\alpha) & 0 \\
    v \cos(\alpha) & 0 \\
    0              & \omega
\end{bmatrix} 
u(t)
$$

,where
$v \in \mathbb{R}$ is a velocity and
$\omega \in \mathbb{R}$ is an angular velocity

3. Two link arm (position based - kinematic control)

$$
x = 
\begin{bmatrix}
    x_1, y_1, x_2, y_2
\end{bmatrix}
$$

$$
\dot{x}(t) =
\begin{bmatrix}
    -l_1 \sin(\theta_1) & 0 \\ 
    l_1 \cos(\theta_1) & 0 \\
    -l_2 \sin(\theta_1 + \theta_2) - l_1 \sin(\theta_1) & -l_2 \sin(\theta_1 + \theta_2) \\ 
    l_2 \cos(\theta_1 + \theta_2) + l_1 \cos(\theta_1) & l_2 \cos(\theta_1 + \theta_2)
\end{bmatrix} 
u(t)
$$

4. Two link arm (angle based - dynamic control)

$$
x = \begin{bmatrix}
    \theta_1, \dot{\theta}_1, \theta_2, \dot{\theta}_2
\end{bmatrix}
$$

$$
\dot{x}(t) = 
\begin{bmatrix} 
    0 & 0 & 1 & 0 \\ 
    0 & 0 & 0 & 1 \\ 
    0 & 0 & 0 & 0 \\ 
    0 & 0 & 0 & 0 \\ 
\end{bmatrix} x(t) + \begin{bmatrix} 
    0 & 0 \\
    0 & 0 \\
    1 & 0 \\
    0 & 1 \\    
\end{bmatrix} 
u(t)
$$
