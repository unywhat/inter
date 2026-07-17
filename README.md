# 🚀 inter  
a very simple 3d space engine built entirely on pygame-ce.

### what is inter?
inter is essentially my first real project that im looking to put on my portfolio. its designed and inspired by games such as space engine, and/or universe sandbox as they are games i've taken a liking to.

### why did i start inter?
i started inter not just because i wanted to add a portfolio project but i also wanted to learn the ins and outs, as well as the dos and donts when it comes to making professional, production ready code.

### ⚠️ status
inter is in VERY early development, expect a multitude of bugs to occur and a lack of features as development continues.

### requirements
- Python 3.11+
- OS: Linux / Windows (untested on macOS)

python dep are installed automagically via `pip install -e .`

### ⚙️ usage / installation
to get started using inter, it's a super easy process. first, download the release (if i've released a executable for the current source version) or download the source code to install it manually.
instructions:

<details>
<summary>if you downloaded the release</summary>
once you've downloaded the release executable, navigate to your downloads folder and double click the executable.
if you would prefer to run it via the terminal, heres how you would do that in linux:

```bash
cd /path/to/your/downloads/ # wherever your downloads folder is
chmod +x ./interX.X.X # version will be different
./interX.X.X # this will launch inter
```
</details>

<details>
<summary>if you downloaded the source</summary>
this tutorial will <strong>not</strong> cover how to make inter into an executable. instead, this will go over how you would run it usually.

steps:
1. download the source (assumed you already done this)
2. extract the .zip
3. open the folder containing the README, pyproject etc. in your terminal of choice
4. run these commands:
```bash
python -m venv .venv
```

5. pick your platform
- if your in powershell (windows):
```ps1
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

- if your in command prompt (windows):
```bat
.\.venv\Scripts\activate.bat
```

- if your in any linux distro:
```bash
source ./.venv/bin/activate
```

6. install dependencies & run
```bash
pip install -e . # install the inter command (NOT global)
inter # this will open inter
```
</details>

### license
MIT -  see [LICENSE](LICENSE) for details.