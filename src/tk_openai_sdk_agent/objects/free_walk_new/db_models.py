from ...database import DbOrmBaseMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String,JSON,DateTime,func,UniqueConstraint
from datetime import datetime

class IpInfoDbOrmDouBaoPro32K(DbOrmBaseMixin):
    __tablename__ = 'n_ip_info_doubao_pro_32k'
    __table_args__ = (
        UniqueConstraint('ip','character', name='unique_ip_character'),
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_0900_ai_ci',
        }
    )
    key_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,comment='主键ID')
    ip: Mapped[str] = mapped_column(String(50),comment='查询的IP名称')
    character: Mapped[str] = mapped_column(String(50),comment='查询的角色名称')
    ai_rsp: Mapped[str] = mapped_column(String(50),comment='验证结果')
    ai_model: Mapped[str] = mapped_column(String(50),comment='AI的模型名称')
    created_at: Mapped[datetime] = mapped_column(DateTime,default=func.now(),comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(DateTime,onupdate=func.now(),nullable=True,comment='更新时间')
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_special_fields(['created_at','updated_at','key_id'])



class IpInfoDbOrmDeepseekV3(DbOrmBaseMixin):
    __tablename__ = 'n_ip_info_deepseek_v3'
    __table_args__ = (
        UniqueConstraint('ip','character', name='unique_ip_character'),
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_0900_ai_ci',
            'schema': 'test_db'
        }
    )

    key_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,comment='主键ID')
    ip: Mapped[str] = mapped_column(String(50),comment='查询的IP名称')
    character: Mapped[str] = mapped_column(String(50),comment='查询的角色名称')
    ai_rsp: Mapped[str] = mapped_column(String(50),comment='AI的回复')
    ai_model: Mapped[str] = mapped_column(String(50),comment='AI的模型名称')
    confidence_level:  Mapped[str] = mapped_column(String(50),comment='置信度')
    basis: Mapped[list] = mapped_column(JSON,comment='依据')
    created_at: Mapped[datetime] = mapped_column(DateTime,default=func.now(),comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(DateTime,onupdate=func.now(),nullable=True,comment='更新时间')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_special_fields(['created_at','updated_at','key_id'])

class IpInfoDbOrmDeepseekR1(DbOrmBaseMixin):
    __tablename__ = 'n_ip_info_deepseek_r1'
    __table_args__ = (
        UniqueConstraint('ip','character', name='unique_ip_character'),
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_0900_ai_ci',
            'schema': 'test_db'
        }
    )

    key_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,comment='主键ID')
    ip: Mapped[str] = mapped_column(String(50),comment='查询的IP名称')
    character: Mapped[str] = mapped_column(String(50),comment='查询的角色名称')
    ai_rsp: Mapped[str] = mapped_column(String(50),comment='AI的回复')
    ai_model: Mapped[str] = mapped_column(String(50),comment='AI的模型名称')
    created_at: Mapped[datetime] = mapped_column(DateTime,default=func.now(),comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(DateTime,onupdate=func.now(),nullable=True,comment='更新时间')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_special_fields(['created_at','updated_at','key_id'])

class IpInfoDbOrmDoubaoThinkPro(DbOrmBaseMixin):
    __tablename__ = 'n_ip_info_doubao_think_pro'
    __table_args__ = (
        UniqueConstraint('ip','character', name='unique_ip_character'),
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_0900_ai_ci',
            'schema': 'test_db'
        }
    )

    key_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,comment='主键ID')
    ip: Mapped[str] = mapped_column(String(50),comment='查询的IP名称')
    character: Mapped[str] = mapped_column(String(50),comment='查询的角色名称')
    ai_rsp: Mapped[str] = mapped_column(String(50),comment='AI的回复')
    ai_model: Mapped[str] = mapped_column(String(50),comment='AI的模型名称')
    created_at: Mapped[datetime] = mapped_column(DateTime,default=func.now(),comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(DateTime,onupdate=func.now(),nullable=True,comment='更新时间')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_special_fields(['created_at','updated_at','key_id'])

class IpInfoDbOrmDoubaoVisionPro(DbOrmBaseMixin):
    __tablename__ = 'n_ip_info_doubao_vision_pro'
    __table_args__ = (
        UniqueConstraint('ip','character', name='unique_ip_character'),
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_0900_ai_ci',
            'schema': 'test_db'
        }
    )

    key_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,comment='主键ID')
    ip: Mapped[str] = mapped_column(String(50),comment='查询的IP名称')
    character: Mapped[str] = mapped_column(String(50),comment='查询的角色名称')
    ai_rsp: Mapped[str] = mapped_column(String(50),comment='AI的回复')
    ai_model: Mapped[str] = mapped_column(String(50),comment='AI的模型名称')
    created_at: Mapped[datetime] = mapped_column(DateTime,default=func.now(),comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(DateTime,onupdate=func.now(),nullable=True,comment='更新时间')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_special_fields(['created_at','updated_at','key_id'])

aimodel_orm_mapping = {
    'DEEPSEEK-V3':IpInfoDbOrmDeepseekV3,
    'DEEPSEEK-R1':IpInfoDbOrmDeepseekR1,
    'DOUBAO-THINKING-PRO':IpInfoDbOrmDoubaoThinkPro,
    'DOUBAO-VISION-PRO':IpInfoDbOrmDoubaoVisionPro,
    'DOUBAO-PRO-32K':IpInfoDbOrmDouBaoPro32K
}
