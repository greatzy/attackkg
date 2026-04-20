#!/usr/bin/env python
import os
import sys

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("========================================")
print("    检查ATT&CK数据导入情况")
print("========================================")
print()

try:
    from app import create_app, db
    app = create_app('development')
    
    with app.app_context():
        # 导入模型
        from app.models.attack import Tactic, Technique, SubTechnique, Mitigation, Software
        
        # 统计数据
        tactic_count = Tactic.query.count()
        technique_count = Technique.query.filter_by(is_subtechnique=False).count()
        subtechnique_count = SubTechnique.query.count()
        mitigation_count = Mitigation.query.count()
        software_count = Software.query.count()
        
        print(f"数据库中共有 {tactic_count} 个战术")
        print(f"数据库中共有 {technique_count} 个技术")
        print(f"数据库中共有 {subtechnique_count} 个子技术")
        print(f"数据库中共有 {mitigation_count} 个缓解措施")
        print(f"数据库中共有 {software_count} 个软件")
        
        # 显示前几个战术
        print("\n前5个战术:")
        tactics = Tactic.query.limit(5).all()
        for tactic in tactics:
            print(f"  {tactic.tactic_id} - {tactic.name}")
        
        # 显示前几个技术
        print("\n前5个技术:")
        techniques = Technique.query.filter_by(is_subtechnique=False).limit(5).all()
        for technique in techniques:
            print(f"  {technique.technique_id} - {technique.name} (战术: {technique.tactic_id})")
        
        print("\n数据检查完成")
        
except Exception as e:
    print(f"检查失败: {str(e)}")
    import traceback
    traceback.print_exc()
