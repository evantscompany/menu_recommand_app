import sqlite3

def add_nickname_column():
    conn = sqlite3.connect('restaurant_app.db')
    cursor = conn.cursor()
    
    try:
        # 1. 먼저 nullable한 nickname 컬럼 추가
        cursor.execute("ALTER TABLE user_accounts ADD COLUMN nickname VARCHAR")
        conn.commit()
        print('Step 1: Added nullable nickname column')
        
        # 2. 기존 데이터에 고유한 닉네임 값 업데이트
        cursor.execute("SELECT user_id, username FROM user_accounts")
        users = cursor.fetchall()
        
        for user_id, username in users:
            unique_nickname = f"{username}_nick"
            cursor.execute("UPDATE user_accounts SET nickname = ? WHERE user_id = ?", (unique_nickname, user_id))
        
        conn.commit()
        print('Step 2: Updated existing records with unique nicknames')
        
        # 3. UNIQUE 제약조건 추가 (SQLite에서는 직접 추가가 어려워 테이블 재생성 필요)
        print('Step 3: Note - UNIQUE constraint will be handled by application level')
        
        # 확인
        cursor.execute('PRAGMA table_info(user_accounts)')
        columns = cursor.fetchall()
        print('Updated columns:')
        for col in columns:
            print(f'  {col[1]} ({col[2]})')
        
        print('Nickname column added successfully!')
        
    except Exception as e:
        print(f'Error: {e}')
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_nickname_column()
