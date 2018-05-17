rm(list=ls())

get.age <- function(birth.str,today.int=20180401){
    b <- as.character(birth.str)
    b <- gsub("-","",b)
    b <- as.numeric(b)
    return( floor((today.int - b) / 10000) )
}


mold.df <- function(df){
    age.min <- 16
    age.max <- 49
    age <- 16:49
    df.tmp <- data.frame(age=age, freq=0)
    df.tmp <- rbind(df,df.tmp)
    freq <- tapply(df.tmp$freq, df.tmp$age, sum)

    df.new <- data.frame(age=as.numeric(names(freq)),freq=freq)

    freq.u15 <- sum(df.new$freq[df.new$age < 16])
    freq.o80 <- df.new$freq[df.new$age > 49]

    df.new <- df.new[df.new$age %in% 16:49, ]
    df.new <- df.new[order(df.new[,1]),]
    
    df.new <- rbind(c("15-",freq.u15), df.new)
    df.new <- rbind(df.new, c("50+",freq.o80))

    df.new$freq <- as.numeric(df.new$freq)

    df.new <- na.omit(df.new)
    return(df.new)
}

d <- read.csv("perf.csv")

d$birthday <- as.Date(d$birthday,format="%Y-%m-%d")

## 活動開始年
d$begin <- c()
x <- tapply(d$year,d$name,min)
y <- data.frame(name=names(x),begin=x)

d2 <- merge(d,y,by="name")
d2 <- d2[d2$category=="テレビアニメ",]
## d2 <- d2[d2$category=="ゲーム",]

library(ggplot2)
library(animation)

k <- 2005:2017
## k <- 2017
col <- rep(rainbow(10),8)
i <- length(col) - 36

saveGIF(
## 年ごとのfor
for( y in k ){
    print(y)
    d.this <- na.omit(d2[d2$year==y,])
    today.int <- as.numeric( paste(as.character(y),"0401",sep="") )

    age <- get.age(d.this$birthday,today.int)

    ## 年齢ごとの出演頻度
    freq <- tapply(d.this$num,age,sum)

    ## 年齢,出演頻度 の data.frame
    freq <- data.frame(age=as.numeric(names(freq)),freq=freq)

    ## データフレームの整形
    freq <- mold.df(freq)

    y.str <- as.character(y)
    g <- ggplot(freq,aes(x=age,y=freq, fill=col[i:(i+35)])) + ggtitle(y.str) + ylim(0,240)
    g <- g + geom_bar(stat = "identity") + guides(fill=FALSE) + theme(axis.text.y = element_text(size=13),axis.text.x = element_text(size=13), axis.title.y = element_text(size=13), title = element_text(size=14))
    g <- g + scale_x_discrete(breaks = c("15-",seq(0,50,5),"50+"))
    print(g)
    i <- i-1
}
, movie.name="animation.gif", ani.width=700)
## d.this[age==19&d.this$year==y,]
