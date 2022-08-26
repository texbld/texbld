{ pkgs ? import <nixpkgs> { } }:
pkgs.python3.pkgs.buildPythonPackage rec {
  pname = "texbld";
  version = "0.4.1";
  src = ./.;
  format = "pyproject";

  propagatedBuildInputs = with pkgs.python3.pkgs; [
    jsonschema
    docker
    requests
    toml
    urllib3
  ];
  buildInputs = with pkgs; [ poetry ];
  meta = with pkgs.lib; {
    homepage = "https://texbld.com";
    description = "A Modern Build Tool for Your Papers";
    license = licenses.gpl3;
  };
  doCheck = false;
}
