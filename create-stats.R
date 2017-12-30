# A very simple example.
crawl <- read.csv(file="out.csv", header=TRUE, sep=",")
plot(crawl$Turns, crawl$Points, xlab="Turns", ylab="Points")
