需要提前安装好subfinder，amass,httpx并配置环境变量  
amass和httpx通过go环境安装  
wget https://go.dev/dl/go1.22.0.linux-amd64.tar.gz  
tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz  
export PATH=$PATH:/usr/local/go/bin  
source ~/.bashrc  
go install -v github.com/owasp-amass/amass/v4/...@latest  
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest  
export PATH="$PATH:subfinder执行程序路径"  
python3 findAsset.py -d xx.com --subfinder --amass -o result.txt
