#!/usr/bin/env python3
"""
🔍 Validador de Arquivos DESSEM

Uso:
    python validate_dessem.py

Este script verifica:
1. Se arquivos pdo_sist.dat e pdo_term.dat existem
2. Se têm o formato correto (separador ;)
3. Se têm número mínimo de colunas
4. Se conseguem ser lidos
5. Amostra de linhas para debug

⚠️ Sem este script, você descobrirá erros apenas rodando o Streamlit!
"""

import os
import sys
from pathlib import Path

def validate_pdo_sist(filepath):
    """Valida arquivo pdo_sist.dat"""
    print(f"\n📄 Validando: {os.path.basename(filepath)}")
    print("-" * 70)
    
    try:
        with open(filepath, "r", encoding="latin1") as f:
            lines = f.readlines()
        
        # Contar linhas
        print(f"✓ Total de linhas: {len(lines)}")
        
        # Procurar linhas válidas
        valid_lines = 0
        iper_min, iper_max = None, None
        
        for i, line in enumerate(lines, 1):
            if ";" not in line:
                continue
            
            p = [x.strip() for x in line.split(";")]
            
            # Verificar tamanho mínimo
            if len(p) < 20:
                continue
            
            # Verificar se primeira coluna é número (IPER)
            if not p[0].isdigit():
                continue
            
            # Linha válida!
            valid_lines += 1
            iper = int(p[0])
            
            if iper_min is None or iper < iper_min:
                iper_min = iper
            if iper_max is None or iper > iper_max:
                iper_max = iper
            
            # Mostrar amostra das primeiras 3 e últimas 2 linhas válidas
            if valid_lines <= 3 or i == len(lines):
                cols_amostra = {
                    "IPER": p[0],
                    "SIST": p[2] if len(p) > 2 else "???",
                    "CMO": p[3] if len(p) > 3 else "???",
                    "DEMANDA": p[4] if len(p) > 4 else "???",
                    "G_RENOV": p[8] if len(p) > 8 else "???",
                    "G_HIDRO": p[9] if len(p) > 9 else "???",
                    "G_TERM": p[10] if len(p) > 10 else "???",
                }
                print(f"  Linha {i}: {cols_amostra}")
        
        print(f"✓ Linhas válidas (com IPER): {valid_lines}")
        if iper_min is not None:
            print(f"✓ Range IPER: {iper_min} → {iper_max}")
        
        # Verificar status
        if valid_lines == 0:
            print("❌ ERRO: Nenhuma linha válida encontrada!")
            print("   Verificar formato (separador ';'?, coluna 0 é número?)")
            return False
        elif valid_lines < 40:
            print(f"⚠️  Aviso: Apenas {valid_lines} IPERs (esperado ~48)")
        else:
            print(f"✅ VÁLIDO: Arquivo tem dados completos")
        
        return True
    
    except FileNotFoundError:
        print(f"❌ ERRO: Arquivo não encontrado: {filepath}")
        return False
    except Exception as e:
        print(f"❌ ERRO ao ler arquivo: {e}")
        return False

def validate_pdo_term(filepath):
    """Valida arquivo pdo_term.dat"""
    print(f"\n📄 Validando: {os.path.basename(filepath)}")
    print("-" * 70)
    
    try:
        with open(filepath, "r", encoding="latin1") as f:
            lines = f.readlines()
        
        print(f"✓ Total de linhas: {len(lines)}")
        
        # Procurar linhas válidas (unid == "99")
        valid_lines = 0
        iper_list = []
        
        for i, line in enumerate(lines, 1):
            if ";" not in line:
                continue
            if any(k in line for k in ("IPER","CustoLinear","MW","---")):
                continue
            
            p = [x.strip() for x in line.split(";")]
            
            if len(p) < 12 or not p[0].isdigit():
                continue
            
            # Linhas com unid == "99"
            if p[4] == "99":
                valid_lines += 1
                iper = int(p[0])
                if iper <= 48:
                    iper_list.append(iper)
                
                # Amostra
                if valid_lines <= 3:
                    cols_amostra = {
                        "IPER": p[0],
                        "NOME": p[3][:20] if len(p) > 3 else "???",
                        "SIST": p[5] if len(p) > 5 else "???",
                        "GERACAO": p[6] if len(p) > 6 else "???",
                    }
                    print(f"  Linha {i}: {cols_amostra}")
        
        print(f"✓ Linhas válidas (unid=99): {valid_lines}")
        if iper_list:
            unique_ipers = len(set(iper_list))
            print(f"✓ IPERs cobertos: {unique_ipers}/48")
        
        if valid_lines == 0:
            print("⚠️  Aviso: Nenhuma linha válida encontrada")
            return False
        else:
            print(f"✅ VÁLIDO: Arquivo tem dados de usinas térmicas")
        
        return True
    
    except FileNotFoundError:
        print(f"⚠️  AVISO: Arquivo não encontrado: {filepath}")
        print("   (Arquivo é OPCIONAL, dashboard funcionará sem ele)")
        return None  # None = arquivo opcional não encontrado
    except Exception as e:
        print(f"❌ ERRO ao ler arquivo: {e}")
        return False

def main():
    print("=" * 70)
    print("🔍 Validador de Arquivos DESSEM")
    print("=" * 70)
    
    # Detectar pasta base
    script_dir = os.path.dirname(os.path.abspath(__file__))
    database_dir = os.path.join(script_dir, "DATABASE")
    
    print(f"\n📍 Pasta base: {script_dir}")
    print(f"📁 Procurando em: {database_dir}")
    print()
    
    # Listar pastas DS_ONS
    if not os.path.exists(database_dir):
        print(f"❌ ERRO: Pasta DATABASE não existe!")
        print(f"   Crie: mkdir DATABASE")
        return 1
    
    dessem_folders = [
        d for d in os.listdir(database_dir)
        if d.startswith("DS_ONS_") and os.path.isdir(os.path.join(database_dir, d))
    ]
    
    if not dessem_folders:
        print(f"❌ ERRO: Nenhuma pasta DS_ONS_* encontrada em DATABASE/")
        print(f"   Copie as pastas de Downloads/")
        return 1
    
    print(f"✓ Encontradas {len(dessem_folders)} pasta(s) DS_ONS_*\n")
    
    # Validar cada pasta
    total_ok = 0
    total_error = 0
    
    for folder_name in sorted(dessem_folders):
        folder_path = os.path.join(database_dir, folder_name)
        
        print(f"\n{'=' * 70}")
        print(f"📂 Pasta: {folder_name}")
        print(f"{'=' * 70}")
        
        arq_sist = os.path.join(folder_path, "pdo_sist.dat")
        arq_term = os.path.join(folder_path, "pdo_term.dat")
        
        # Validar pdo_sist.dat (OBRIGATÓRIO)
        if not validate_pdo_sist(arq_sist):
            total_error += 1
            continue
        
        # Validar pdo_term.dat (OPCIONAL)
        result_term = validate_pdo_term(arq_term)
        
        # Status final
        status = "✅ PRONTO" if (result_term is None or result_term) else "⚠️  PARCIAL"
        print(f"\n{status} para usar com o Streamlit")
        total_ok += 1
    
    # Relatório final
    print(f"\n\n{'=' * 70}")
    print(f"📊 Relatório Final")
    print(f"{'=' * 70}")
    print(f"✓ Pastas válidas: {total_ok}/{len(dessem_folders)}")
    print(f"❌ Pastas com erro: {total_error}/{len(dessem_folders)}")
    print()
    
    if total_error == 0:
        print("🎉 Tudo OK! Pronto para rodar:")
        print("   streamlit run presentacion_app.py")
        return 0
    else:
        print("⚠️  Alguns arquivos têm problemas. Verifique acima.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
