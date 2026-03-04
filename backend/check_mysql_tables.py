"""
TiDB Cloud 테이블 확인
"""

import os
from sqlalchemy import create_engine, text

def check_mysql_tables():
    """MySQL 테이블 확인"""
    try:
        # 환경 변수 설정
        os.environ["TIDB_HOST"] = "gateway01.ap-northeast-1.prod.aws.tidbcloud.com"
        os.environ["TIDB_PORT"] = "4000"
        os.environ["TIDB_USER"] = "3bJdto8FKWk47Fu.root"
        os.environ["TIDB_PASSWORD"] = "NWOZOcYDO8W5nMk2"
        os.environ["TIDB_DATABASE"] = "test"
        
        # 연결
        engine = create_engine(
            f"mysql+pymysql://3bJdto8FKWk47Fu.root:NWOZOcYDO8W5nMk2@gateway01.ap-northeast-1.prod.aws.tidbcloud.com:4000/test?charset=utf8mb4&ssl=true"
        )
        
        with engine.connect() as conn:
            # 테이블 목록 조회
            result = conn.execute(text("SHOW TABLES"))
            tables = []
            for row in result:
                tables.append(row[0])
            
            print("📋 TiDB Cloud 테이블 목록:")
            for table in tables:
                print(f"  - {table}")
            
            # 각 테이블의 레코드 수 확인
            for table in tables:
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    print(f"  {table}: {count}개 레코드")
                except Exception as e:
                    print(f"  {table}: 확인 실패 - {e}")
        
        return tables
        
    except Exception as e:
        print(f"❌ MySQL 확인 실패: {e}")
        return []

if __name__ == "__main__":
    check_mysql_tables()
