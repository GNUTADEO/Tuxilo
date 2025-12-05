#{ pkgs ? import <nixpkgs> {} }:
#
#let e =
#  pkgs.buildFHSEnv {
#    name = "gcc-git-build-env";
#    targetPkgs = ps: with ps; [
#      gcc
#      stdenv.cc
#      stdenv
#      pkg-config
#      zlib
#      gdal
#      geos
#      proj
#    ];
#  };
#in e.env




{
  description = "Camara 2026 Dev Environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };

        python = pkgs.python312;
        py = python.withPackages (ps: with ps; [
          pandas
          geopandas
          shapely
          pyzmq
          jupyter
          notebook
          ipykernel
          pyarrow
          folium
          branca
          mapclassify
        ]);
      in {
        devShells.default = pkgs.mkShell {
          name = "camara-2026";

          packages = [
            py     # ← all big libs here; no wheels
            pkgs.uv
            pkgs.git
            pkgs.gdal
            pkgs.geos
            pkgs.proj
            pkgs.zeromq
          ];

          # Make sure CPython always resolves THIS python
          PYTHONPATH="${py}/${python.sitePackages}";

          shellHook = ''
            echo "[camara-2026] Python: $(python --version)"
            echo "Using Nix-provided scientific stack (no wheel builds)"
          '';
        };
      });
}
