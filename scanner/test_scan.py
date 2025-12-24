from scanner.banner_grabber import grab_banner

target = "172.16.0.1"
port = 8099

banner = grab_banner(target, port)
print("Resultado:", banner)
