"""
CIAS-X AI Scientist - Data Models
Based on Kosmos world model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import json

Base = declarative_base()

class CIASDesign(Base):
    """设计表 - 对应一次完整的设计周期"""
    __tablename__ = 'cias_designs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    design_name = Column(String(255), nullable=False)
    objective = Column(Text, nullable=False)  # 研究目标
    design_space = Column(JSON, nullable=False)  # 设计空间定义
    budget_max = Column(Integer, default=100)  # 最大实验预算
    budget_used = Column(Integer, default=0)  # 已使用预算
    status = Column(String(50), default='INITIALIZING')  # INITIALIZING, RUNNING, COMPLETED, FAILED
    trends = Column(Text, nullable=True)  # LLM总结的趋势
    pareto_front = Column(JSON, nullable=True)  # Pareto前沿
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    experiments = relationship("CIASExperiment", back_populates="design", cascade="all, delete-orphan")

class CIASExperiment(Base):
    """实验表 - 一次设计包含多个实验"""
    __tablename__ = 'cias_experiments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    design_id = Column(Integer, ForeignKey('cias_designs.id'), nullable=False)
    experiment_name = Column(String(255), nullable=False)
    cycle_number = Column(Integer, nullable=False)  # 第几个循环
    status = Column(String(50), default='PENDING')  # PENDING, RUNNING, COMPLETED, FAILED
    llm_summary = Column(Text, nullable=True)  # 实验的LLM总结
    metadata = Column(JSON, nullable=True)  # 额外元数据
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # 关系
    design = relationship("CIASDesign", back_populates="experiments")
    configurations = relationship("CIASConfiguration", back_populates="experiment", cascade="all, delete-orphan")

class CIASConfiguration(Base):
    """配置表 - 一个实验包含多个配置"""
    __tablename__ = 'cias_exp_configurations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    experiment_id = Column(Integer, ForeignKey('cias_experiments.id'), nullable=False)
    config_name = Column(String(255), nullable=False)

    # Forward Model配置
    forward_config = Column(JSON, nullable=False)  # T, dose, compression, mask_type等

    # Reconstruction配置
    recon_family = Column(String(100), nullable=False)  # CIAS-Core, CIAS-Core-ELP等
    recon_params = Column(JSON, nullable=False)  # 网络参数

    # UQ配置
    uq_scheme = Column(String(100), nullable=True)  # Conformal, Ensemble等
    uq_params = Column(JSON, nullable=True)

    # Training配置
    train_config = Column(JSON, nullable=False)  # learning_rate, epochs等

    status = Column(String(50), default='PENDING')
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    experiment = relationship("CIASExperiment", back_populates="configurations")
    analysis = relationship("CIASAnalysis", back_populates="configuration", uselist=False, cascade="all, delete-orphan")
    artifacts = relationship("CIASArtifact", back_populates="configuration", cascade="all, delete-orphan")

class CIASAnalysis(Base):
    """分析表 - 存储单次训练的评估指标"""
    __tablename__ = 'cias_exp_analysis'

    id = Column(Integer, primary_key=True, autoincrement=True)
    config_id = Column(Integer, ForeignKey('cias_exp_configurations.id'), nullable=False, unique=True)

    # 性能指标
    psnr = Column(Float, nullable=True)
    ssim = Column(Float, nullable=True)
    coverage = Column(Float, nullable=True)  # UQ覆盖率
    calibration_error = Column(Float, nullable=True)
    latency = Column(Float, nullable=True)  # 推理延迟

    # 其他指标
    metrics = Column(JSON, nullable=True)  # 额外指标的JSON存储

    llm_summary = Column(Text, nullable=True)  # 对此次运行的LLM总结
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    configuration = relationship("CIASConfiguration", back_populates="analysis")

class CIASArtifact(Base):
    """产物表 - 存储训练产生的文件路径"""
    __tablename__ = 'cias_exp_artifacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    config_id = Column(Integer, ForeignKey('cias_exp_configurations.id'), nullable=False)

    artifact_type = Column(String(100), nullable=False)  # checkpoint, video, log, figure等
    file_path = Column(String(512), nullable=False)
    file_size = Column(Integer, nullable=True)  # 字节
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    configuration = relationship("CIASConfiguration", back_populates="artifacts")

# 数据库初始化函数
def init_database(db_url='sqlite:///cias_scientist.db'):
    """初始化数据库"""
    engine = create_engine(db_url, echo=False)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    """获取数据库会话"""
    Session = sessionmaker(bind=engine)
    return Session()
