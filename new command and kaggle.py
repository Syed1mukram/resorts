git add .
git commit -m "Fix timeline using actual audio duration"
git push

%cd /kaggle/working
!rm -rf resorts
!git clone https://github.com/Syed1mukram/resorts.git
%cd resorts
!pip install -q -r requirements.txt
!python main.py



git add .
git commit -m "New hotel"
git push

!rm -rf /kaggle/working/resorts
!git clone https://github.com/Syed1mukram/resorts.git
%cd resorts
!python main.py