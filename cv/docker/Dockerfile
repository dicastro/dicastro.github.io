FROM pandoc/latex:3.6.4.0-alpine

RUN tlmgr option repository http://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2024/tlnet-final && \
    tlmgr update --self && \
    tlmgr install moderncv qrcode xkeyval tikzmark enumitem

RUN curl -s -L https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2024/tlnet-final/archive/lm.tar.xz -o /tmp/lm.tar.xz && \
    mkdir -p /usr/share/fonts/OTF/latin-modern && \
    tar --extract --file=/tmp/lm.tar.xz --xz --wildcards --strip-components=4 --directory=/usr/share/fonts/OTF/latin-modern fonts/opentype/public/lm/*.otf && \
    fc-cache -f -v /usr/share/fonts/OTF/latin-modern && \
    rm -rf /tmp/lm.tar.xz && \
    curl -s -L https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2024/tlnet-final/archive/lm-math.tar.xz -o /tmp/lm-math.tar.xz && \
    mkdir -p /usr/share/fonts/OTF/latin-modern-math && \
    tar --extract --file=/tmp/lm-math.tar.xz --xz --wildcards --strip-components=4 --directory=/usr/share/fonts/OTF/latin-modern-math fonts/opentype/public/lm-math/*.otf && \
    fc-cache -f -v /usr/share/fonts/OTF/latin-modern-math && \
    rm -rf /tmp/lm-math.tar.xz && \
    curl -s -L https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2024/tlnet-final/archive/fira.tar.xz -o /tmp/fira.tar.xz && \
    mkdir -p /usr/share/fonts/OTF/fira && \
    tar --extract --file=/tmp/fira.tar.xz --xz --wildcards --strip-components=4 --directory=/usr/share/fonts/OTF/fira fonts/opentype/public/fira/*.otf && \
    fc-cache -f -v /usr/share/fonts/OTF/fira && \
    rm -rf /tmp/fira.xz