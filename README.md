# SA_Group8

有集合app至同一資料夾 "apps"
  settings加入:
    BASE_DIR = Path(__file__).resolve().parent.parent
    sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

有git ignore，但有留migrations資料夾（資料庫模型紀錄檔）
跑django不影響，直接runserver就好
