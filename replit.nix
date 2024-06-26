{pkgs}: {
  deps = [
    pkgs.unixtools.ping
    pkgs.openssh
    pkgs.glibcLocales
    pkgs.postgresql
  ];
}