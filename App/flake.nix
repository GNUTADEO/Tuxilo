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

        python = pkgs.python314;
        py = python.withPackages (ps: with ps; [
        ]);
      in {
        devShells.default = pkgs.mkShell {
          name = "camara-2026";

          packages = [
            py     # ← all big libs here; no wheels
            pkgs.uv
          ];

          # Make sure CPython always resolves THIS python
          PYTHONPATH="${py}/${python.sitePackages}";
        };
      });
}
