{
  description = "Nix Flake for my AE 8900 project.";

  # Flake inputs
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs"; # also valid: "nixpkgs"
  };

  # Flake outputs
  outputs = { self, nixpkgs }:
    let
      # Systems supported
      allSystems = [
        "x86_64-linux" # 64-bit Intel/AMD Linux
        "aarch64-linux" # 64-bit ARM Linux
      ];

      # Helper to provide system-specific attributes
      forAllSystems = f:
        nixpkgs.lib.genAttrs allSystems
        (system: f { pkgs = import nixpkgs { inherit system; }; });
    in {
      # Development environment output
      devShells = forAllSystems ({ pkgs }: {
        default = let
          daqhats = pkgs.python3Packages.buildPythonPackage {
            name = "daqhats";
            version = "1.4.0.4";
            src = pkgs.fetchFromGitHub {
              owner = "mccdaq";
              repo = "daqhats";
              rev = "e6d96c8fb621c83696536a037f1c4fa373c46068";
              sha256 = "7+KEbyvmHCsT9O90V2mGDe6OWU8sQmVph5BHN9e4xj0=";
            };
            doCheck = false;

          };
          # use Python 3.11
          python = pkgs.python311;
        in pkgs.mkShell {

          # the Nix packages provided in the environment
          packages = [
            # python and necessary packages
            (python.withPackages (ps:
              with ps; [
                black
                fastapi
                flit
                isort
                pip
                psutil
                python-dotenv
                smbus2
                uvicorn
                websockets
              ]))
            daqhats
            pkgs.nixfmt
            pkgs.ruff
            pkgs.tmux
            pkgs.tmuxp
            pkgs.just
            pkgs.nodejs_20
            pkgs.nodePackages_latest.pnpm
          ];

          shellHook = ''
            cd frontend && pnpm install && cd ..
            echo -e "\e[1;3;32mAE 8900 development environment active!\e[0m"
            # this might introduce... side effects.
            if [ -n "$IN_NIX_SHELL" ]; then
                exec $SHELL
            fi
          '';

        };
      });
    };
}
