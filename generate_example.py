# generate_example.py

# Imports
import argparse
import json
import numpy as np
import scipy.spatial

from uniform_bspline import Contour


# main
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('degree', type=int)
    parser.add_argument('num_control_points', type=int)
    parser.add_argument('num_data_points', type=int)
    parser.add_argument('output_path')
    parser.add_argument('--dim', type=int, choices={2, 3}, default=2)
    parser.add_argument('--num-init-points', type=int, default=16)
    parser.add_argument('--sigma', type=float, default=0.05)
    parser.add_argument('--seed', type=int)
    args = parser.parse_args()

    x = np.linspace(0.0, 2.0 * np.pi, args.num_data_points)
    y = np.exp(-x / (2.0 * np.pi)) * np.sin(3.0 * x)

    if args.dim == 2:
        Y = np.c_[x, y]
    else:
        Y = np.c_[x, y, np.linspace(0.0, 1.0, args.num_data_points)]

    x0, x1 = Y[0].copy(), Y[-1].copy()
    t = np.linspace(0.0, 1.0, args.num_control_points)[:, np.newaxis]
    X = x0 * (1 - t) + x1 * t

    if args.seed is not None:
        np.random.seed(args.seed)
    Y += args.sigma * np.random.randn(Y.size).reshape(Y.shape)
    w = np.ones(args.num_data_points, dtype=float)

    c = Contour(args.degree, args.num_control_points, args.dim)
    u0 = c.uniform_parameterisation(args.num_init_points)
    D = scipy.spatial.distance.cdist(Y, c.M(u0, X))
    u = u0[D.argmin(axis=1)]

    to_list = lambda _: _.tolist()
    z = dict(degree=args.degree,
             num_control_points=args.num_control_points,
             dim=args.dim,
             is_closed=False,
             Y=to_list(Y),
             w=to_list(w),
             u=to_list(u),
             X=to_list(X))

    print 'Output:', args.output_path
    with open(args.output_path, 'wb') as fp:
        fp.write(json.dumps(z, indent=4))


if __name__ == '__main__':
    main()