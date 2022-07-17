{ pkgs ? import <nixpkgs> {} }:
pkgs.python3.pkgs.buildPythonPackage rec {
  pname = "texbld";
  version = "0.3.0";
  src = pkgs.python3.pkgs.fetchPypi {
    inherit pname version;
    sha256 = "1xl5j0g1d2i6v17i7g6l8kv96zk8fq5jjdjlafr7c8br85ih277z";
  };

  propagatedBuildInputs = with pkgs.python3.pkgs;
      [jsonschema docker requests toml urllib3];
  buildInputs = with pkgs; [poetry];
  meta = with pkgs.lib; {
    homepage = "https://texbld.com";
    description = "A Modern Build Tool for Your Papers";
    license = licenses.gpl3;
  };
  doCheck = false;
}
