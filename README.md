# 🚀 RocketDrive Developer Guide

## 🛠 Building the Images

You can build either the **demo** or **live** images using `make`:

Demo are to be released to competitors for analysis
Live is run in the target environment and contains a flag

### **Build Demo Image**
```sh
make demo
```
This will:
- Initialize the demo database (`init_demo_db.py`)
- Replace `app/files/` with `demo_files/`
- Build the `demo` Docker image
- Tag and commit it to `tjoconnor/rocketdrive-demo`

### **Build Live Image**
```sh
make live
```
This will:
- Initialize the live database (`init_live_db.py`)
- Replace `app/files/` with `live_files/`
- Build the `live` Docker image
- Tag and commit it to `tjoconnor/rocketdrive-live`
- Save the built image as `live-image`

---

## 🏃 Running the CTF Images

Once built, you can run either the demo or live images:

### **Run the Demo Image**
```sh
docker run -p 8000:80 demo
```
### **Run the Live Image**
```sh
docker run -p 8000:80 live
```
The application will be accessible at:
🌍 **http://127.0.0.1:8000**

---

## 🛰️ Pulling Prebuilt Images from DockerHub
If you don't want to build the images manually, you can pull the prebuilt ones:

### **Pull and Run Demo Image**
```sh
docker pull tjoconnor/rocketdrive-demo
docker run -p 8000:80 tjoconnor/rocketdrive-demo
```

### **Pull and Run Live Image**
```sh
docker pull tjoconnor/rocketdrive-live
docker run -p 8000:80 tjoconnor/rocketdrive-live
```

---

## 🔓 Cracking the Hashes
A script exists for brute-forcing stored hashes:
```sh
solution/brute-force-hash.py
```
This script will attempt to crack stored password hashes in the challenge. Note, there is a high-rate of collisions due to the poor algorithm implementation. The recovered password will work but may not be the original password. 

```
python3 solution/brute-force-hash.py 
[*] Starting brute-force attack against interim ~salt~...
[*] Using 14 processes for brute force.
Searching: 2013492816873 attempts [00:29, 101327565997.74 attempts/s]                                                                                                                                                                                     
[+] Salt Found: 336592370
Searching: 2025921388053 attempts [00:29, 68485763188.37 attempts/s] 
[*] Starting un~salting~ attack...
[+] Recovered salt...
Password Recovered gbilz
```