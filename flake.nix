{
  description = "A nix-flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
        supportedSystems = [ "x86_64-linux" ];
        forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
            pkgs = import nixpkgs { inherit system; };
        });
    in
    {
        devShells = forEachSupportedSystem({ pkgs }: {
            default = pkgs.mkShell.override {
                stdenv = pkgs.gccStdenv;
            }
            {
                packages = with pkgs; [
                    cmake
                    boost
                    python311
                ] ++
                (with pkgs.python311Packages; [
                    pybind11
                    tkinter
                    pandas
                    numpy
                    matplotlib
                ]);
            };
        });
    };
}
