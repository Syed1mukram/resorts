git add .
git commit -m "Fix timeline using actual audio duration"
git push

%cd /kaggle/working
!rm -rf resorts
!git clone https://github.com/Syed1mukram/resorts.git
%cd resorts
!pip install -q -r requirements.txt
!python main.py



git add input
git commit -m "New hotel"
git push

cd /kaggle/working && \
rm -rf resorts && \
git clone https://github.com/Syed1mukram/resorts.git && \
cd resorts && \
python main.py


-----------

git add input
git commit -m "New hotel"
git push



%%bash
pip install -q faster-whisper ctranslate2 open-clip-torch python-dotenv

%%bash

cd /kaggle/working
rm -rf resorts
git clone https://github.com/Syed1mukram/resorts.git
cd resorts

python -u main.py


%cd /kaggle/working

!rm -rf resorts

!git clone https://github.com/Syed1mukram/resorts.git

%cd resorts

!python main.py

-------------------

file change :

git add .
git commit -m "New hotel"
git push

----------
Git ko farq nahi padta, lekin baad me history dekhte waqt meaningful message zyada useful hote hain.

git add .
git commit -m "."
git push