.class public LHello;
.super Ljava/lang/Object;


# instance fields
.field private who:Ljava/lang/String; 


# static fields


# direct methods
.method public constructor <init>(Ljava/lang/String;)V
    invoke-direct {v0}, Ljava/lang/Object.<init>()V ; 0x4

    iput-object v1, v0, LHello;->who Ljava/lang/String;

    return-void

.method public static main([Ljava/lang/String;)V
    new-instance v0, LHello;

    const-string v1, str.World

    invoke-direct {v0, v1}, LHello.<init>(Ljava/lang/String;)V ; 0x0

    invoke-virtual {v0}, LHello.say()V ; 0x2

    return-void


# virtual methods
.method public say()V
    sget-object v0, Ljava/lang/System;->out Ljava/io/PrintStream;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder.<init>()V ; 0x5

    const-string v2, str.Hello

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder.append(Ljava/lang/String;)Ljava/lang/StringBuilder; ; 0x6

    move-result-object v1

    iget-object v2, v3, LHello;->who Ljava/lang/String;

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder.append(Ljava/lang/String;)Ljava/lang/StringBuilder; ; 0x6

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder.toString()Ljava/lang/String; ; 0x7

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/io/PrintStream.println(Ljava/lang/String;)V ; 0x3

    return-void

