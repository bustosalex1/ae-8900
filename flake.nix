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

      # github source for the daqhats library and python package
      daqhatsSrc = { pkgs }:
        pkgs.fetchFromGitHub {
          owner = "mccdaq";
          repo = "daqhats";
          rev = "e6d96c8fb621c83696536a037f1c4fa373c46068";
          sha256 = "7+KEbyvmHCsT9O90V2mGDe6OWU8sQmVph5BHN9e4xj0=";
        };
    in {
      packages = forAllSystems ({ pkgs }: {
        libdaqhats = pkgs.stdenv.mkDerivation {
          pname = "libdaqhats";
          version = "1.4.0.6";

          src = daqhatsSrc { inherit pkgs; };

          buildInputs = with pkgs; [ gcc autoPatchelfHook libraspberrypi ];

          propagatedBuildInputs = [ pkgs.glibc ];

          postPatch = ''
            substituteInPlace lib/makefile \
              --replace 'INSTALL_DIR = /usr/local/lib' 'INSTALL_DIR = \$\(out\)/lib' \
              --replace 'ldconfig' '# ldconfig'

            substituteInPlace include/makefile \
              --replace 'INSTALL_DIR = /usr/local/include' 'INSTALL_DIR = \$\(out\)/include'
          '';

          buildPhase = ''
            make -C lib all
          '';

          installPhase = ''
            mkdir -p $out/lib
            cp lib/build/libdaqhats.so.$version $out/lib/libdaqhats.so.$version
            ln -s $out/lib/libdaqhats.so.$version $out/lib/libdaqhats.so
            ln -s $out/lib/libdaqhats.so.$version $out/lib/libdaqhats.so.1
          '';
          dontStrip = true;

        };

        daqhats = pkgs.python3Packages.buildPythonPackage {
          name = "daqhats";
          version = "1.4.0.4";
          src = daqhatsSrc { inherit pkgs; };
          doCheck = false;

          postPatch = ''
            substituteInPlace daqhats/hats.py \
              --replace 'libdaqhats.so.1' \
              '${self.packages.${pkgs.system}.libdaqhats}/lib/libdaqhats.so.1'
          '';

        };
      });

      # Development environment output
      devShells = forAllSystems ({ pkgs }: {
        default = let
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
            self.packages.${pkgs.system}.daqhats
            pkgs.nixfmt
            pkgs.sc-im
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
