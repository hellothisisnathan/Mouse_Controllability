library(ggpubr)
files <- list.files(path="C:/Users/Nathan/OneDrive/School Work/Hommel Lab/Mouse_Controllability/Mouse/whole brain/csv/", pattern="*.csv", full.names=TRUE, recursive=FALSE)
ieadft.100 <- read.csv(files[1])
ieadft.50 <- read.csv(files[2])
adft.100 <- read.csv(files[3])
adft.50 <- read.csv(files[4])
adftzi.100 <- read.csv(files[5])
adftzi.50 <- read.csv(files[6])
ldft.100 <- read.csv(files[7])
ldft.50 <- read.csv(files[8])
ldftzi.100 <- read.csv(files[9])
ldftzi.50 <- read.csv(files[10])

# Communicating edges = Outgoing edges + incoming edges
adft.50.plot <- ggscatter(adft.50, x = "avg.dft", y = "outgoing.incoming", add = "reg.line", conf.int = TRUE, cor.coef = TRUE, color = "blue")
adft.50.plot <- adft.50.plot + labs(x = "Average Distance from True", y = "# communicating edges", title = "# Communicating edges vs avg DFT 50%")
adft.50.plot
adft.100.plot <- ggscatter(adft.100, x = "avg.dft", y = "outgoing.incoming", add = "reg.line", conf.int = TRUE, cor.coef = TRUE, color = "blue")
adft.100.plot <- adft.100.plot + labs(x = "Average Distance from True", y = "# communicating edges", title = "# Communicating edges vs avg DFT 100%")
adft.100.plot

adftzi.50.plot <- ggscatter(adftzi.50, x = "avg.dft", y = "outgoing.incoming", add = "reg.line", conf.int = TRUE, cor.coef = TRUE, color = "#00adad")
adftzi.50.plot <- adftzi.50.plot + labs(x = "Average Distance from True", y = "# communicating edges", title = "# Communicating edges vs avg DFT - ZI removed 50%") + theme(text=element_text(family="ArialMT", size=10))
adftzi.50.plot
adftzi.100.plot <- ggscatter(adftzi.100, x = "avg.dft", y = "outgoing.incoming", add = "reg.line", conf.int = TRUE, cor.coef = TRUE, color = "#00adad")
adftzi.100.plot <- adftzi.100.plot + labs(x = "Average Distance from True", y = "# communicating edges", title = "# Communicating edges vs avg DFT - ZI removed 100%") + theme(text=element_text(family="ArialMT", size=10))
adftzi.100.plot

ieadft.50.plot <- ggscatter(ieadft.50, x = "avg.dft", y = "outgoing.incoming...internal", add = "reg.line", conf.int = TRUE, cor.coef = TRUE, color = "#faaa16")
ieadft.50.plot <- ieadft.50.plot + labs(x = "Average Distance from True", y = "(# communicating edges) / (# internal edges)", title = "(# Communicating edges) / (# internal edges) vs avg DFT 50%") + theme(text=element_text(family="ArialMT", size=10))
ieadft.50.plot
ieadft.100.plot <- ggscatter(ieadft.100, x = "avg.dft", y = "outgoing.incoming...internal", add = "reg.line", conf.int = TRUE, cor.coef = TRUE, color = "#faaa16")
ieadft.100.plot <- ieadft.100.plot + labs(x = "Average Distance from True", y = "(# communicating edges) / (# internal edges)", title = "(# Communicating edges) / (# internal edges) vs avg DFT 100%") + theme(text=element_text(family="ArialMT", size=10))
ieadft.100.plot

ldft.50.plot <- ggscatter(ldft.50, x = "largest.dft", y = "outgoing.incoming", add = "reg.line", conf.int = TRUE, cor.coef = TRUE, color = "#1d471d")
ldft.50.plot <- ldft.50.plot + labs(x = "Largest Distance from True", y = "# communicating edges", title = "# Communicating edges vs largest DFT 50%")
ldft.50.plot
ldft.100.plot <- ggscatter(ldft.100, x = "largest.dft", y = "outgoing.incoming", add = "reg.line", conf.int = TRUE, cor.coef = TRUE, color = "#1d471d")
ldft.100.plot <- ldft.100.plot + labs(x = "Largest Distance from True", y = "# communicating edges", title = "# Communicating edges vs largest DFT 100%")
ldft.100.plot

ldftzi.50.plot <- ggscatter(ldftzi.50, x = "largest.dft", y = "outgoing.incoming", add = "reg.line", conf.int = TRUE, cor.coef = TRUE, color = "#00c000")
ldftzi.50.plot <- ldftzi.50.plot + labs(x = "Largest Distance from True", y = "# communicating edges", title = "# Communicating edges vs largest DFT - ZI removed 50%") + theme(text=element_text(family="ArialMT", size=10))
ldftzi.50.plot
ldftzi.100.plot <- ggscatter(ldftzi.100, x = "largest.dft", y = "outgoing.incoming", add = "reg.line", conf.int = TRUE, cor.coef = TRUE, color = "#00c000")
ldftzi.100.plot <- ldftzi.100.plot + labs(x = "Largest Distance from True", y = "# communicating edges", title = "# Communicating edges vs largest DFT - ZI removed 100%") + theme(text=element_text(family="ArialMT", size=10))
ldftzi.100.plot

ggarrange(adft.50.plot, adft.100.plot + rremove("ylab"), ncol = 2, nrow = 1)
ggsave(file="C:/Users/Nathan/OneDrive/School Work/Hommel Lab/Mouse_Controllability/Mouse/whole brain/graphs/communicating edges vs avg dft.png", width = 10, height = 5, dpi=500)
ggarrange(adftzi.50.plot, adftzi.100.plot + rremove("ylab"), ncol = 2, nrow = 1)
ggsave(file="C:/Users/Nathan/OneDrive/School Work/Hommel Lab/Mouse_Controllability/Mouse/whole brain/graphs/communicating edges vs avg dft no ZI.png", width = 10, height = 5, dpi=500)
ggarrange(ieadft.50.plot, ieadft.100.plot + rremove("ylab"), ncol = 2, nrow = 1)
ggsave(file="C:/Users/Nathan/OneDrive/School Work/Hommel Lab/Mouse_Controllability/Mouse/whole brain/graphs/communicating edges per internal edges vs avg dft.png", width = 10, height = 5, dpi=500)
ggarrange(ldft.50.plot, ldft.100.plot + rremove("ylab"), ncol = 2, nrow = 1)
ggsave(file="C:/Users/Nathan/OneDrive/School Work/Hommel Lab/Mouse_Controllability/Mouse/whole brain/graphs/communicating edges vs largest dft.png", width = 10, height = 5, dpi=500)
ggarrange(ldftzi.50.plot, ldftzi.100.plot + rremove("ylab"), ncol = 2, nrow = 1)
ggsave(file="C:/Users/Nathan/OneDrive/School Work/Hommel Lab/Mouse_Controllability/Mouse/whole brain/graphs/communicating edges vs largest dft no ZI.png", width = 10, height = 5, dpi=500)
# ggarrange(ieadft.50.plot, ieadft.100.plot + rremove("ylab"),adft.50.plot, adft.100.plot + rremove("ylab"), adftzi.50.plot, adftzi.100.plot + rremove("ylab"), ldft.50.plot, ldft.100.plot + rremove("ylab"), ldftzi.50.plot, ldftzi.100.plot + rremove("ylab"), ncol = 2, nrow = 5)
# ggsave(file="C:/Users/Nathan/OneDrive/School Work/Hommel Lab/Mouse_Controllability/Mouse/whole brain/graphs/graph grid.png", width = 5, height = 8, dpi=500)