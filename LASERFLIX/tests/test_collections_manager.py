"""
test_collections_manager.py — Testes agressivos para encontrar bugs reais.

Estratégia: bordas, injeção de dados inválidos, comportamento após corrupção.
"""
import json
import os
import pytest
from core.collections_manager import CollectionsManager


# ══════════════════════════════════════════════════════════════
# FIXTURES
# ══════════════════════════════════════════════════════════════

@pytest.fixture
def cm(tmp_path):
    return CollectionsManager(file_path=str(tmp_path / "collections.json"))


# ══════════════════════════════════════════════════════════════
# INTEGRIDADE — dados que entram têm que sair iguais
# ══════════════════════════════════════════════════════════════

class TestIntegridade:

    def test_get_projects_retorna_referencia_interna_mutavel(self, cm):
        """Bug: get_projects() retorna a lista interna — modificar fora corrompe a coleção."""
        cm.create_collection("Favoritos")
        cm.add_project("Favoritos", "/path/a")
        lista = cm.get_projects("Favoritos")
        lista.append("/INVASÃO")  # modifica o retorno
        projetos = cm.get_projects("Favoritos")
        assert "/INVASÃO" not in projetos, (
            "BUG: get_projects() retorna referência à lista interna. "
            "Modificar o retorno corrompe a coleção silenciosamente."
        )

    def test_save_load_preserva_projetos_com_paths_unicode(self, cm):
        """Paths com caracteres especiais (acentos, espaços) devem sobreviver save/load."""
        cm.create_collection("São Paulo")
        cm.add_project("São Paulo", "C:/Users/Família/Projeto São João")
        cm.load()  # recarrega do disco
        projetos = cm.get_projects("São Paulo")
        assert "C:/Users/Família/Projeto São João" in projetos, (
            "BUG: path com caracteres unicode corrompido após save/load."
        )

    def test_save_load_preserva_multiplas_colecoes(self, cm):
        """Múltiplas coleções com muitos projetos devem ser preservadas integralmente."""
        for i in range(20):
            cm.create_collection(f"Coleção {i}")
            for j in range(50):
                cm.add_project(f"Coleção {i}", f"/path/projeto_{i}_{j}")
        cm.load()
        assert len(cm.get_all_collections()) == 20, "Número de coleções mudou após reload"
        assert cm.get_collection_size("Coleção 5") == 50, "Projetos perdidos após reload"


# ══════════════════════════════════════════════════════════════
# DADOS INVÁLIDOS — o que o usuário / sistema pode causar
# ══════════════════════════════════════════════════════════════

class TestDadosInvalidos:

    def test_create_collection_com_apenas_espacos(self, cm):
        """Nome com só espaços deve ser rejeitado (strip + validação)."""
        resultado = cm.create_collection("     ")
        assert resultado is False, (
            "BUG: create_collection('     ') retornou True. "
            "Coleção com nome vazio/espaços criada no banco."
        )
        assert "     " not in cm.get_all_collections()
        assert "" not in cm.get_all_collections()

    def test_create_collection_nome_muito_longo(self, cm):
        """Nome com 10.000 caracteres não pode travar ou corromper o arquivo."""
        nome_gigante = "A" * 10000
        try:
            cm.create_collection(nome_gigante)
            cm.save()
            cm.load()
        except Exception as e:
            pytest.fail(f"BUG: nome gigante causou exceção: {e}")

    def test_add_project_path_vazio(self, cm):
        """Path vazio não deve ser adicionado a uma coleção."""
        cm.create_collection("Teste")
        resultado = cm.add_project("Teste", "")
        assert resultado is False, (
            "BUG: add_project aceita path vazio. "
            "Projetos fantasmas na coleção."
        )
        assert "" not in cm.get_projects("Teste")

    def test_add_project_path_none(self, cm):
        """Path None não deve ser aceito nem causar AttributeError."""
        cm.create_collection("Teste")
        try:
            resultado = cm.add_project("Teste", None)
            assert resultado is False, "BUG: add_project(None) retornou True"
        except (AttributeError, TypeError) as e:
            pytest.fail(f"BUG: add_project(None) lança exceção: {e}")

    def test_rename_para_nome_com_apenas_espacos(self, cm):
        """Renomear para nome vazio/espaços deve ser rejeitado."""
        cm.create_collection("Original")
        resultado = cm.rename_collection("Original", "   ")
        assert resultado is False, (
            "BUG: rename_collection para '   ' (só espaços) retornou True. "
            "Coleção ficou com nome vazio."
        )
        assert "Original" in cm.get_all_collections(), "Coleção original desapareceu"

    def test_colecao_com_projeto_duplicado_via_arquivo_externo(self, tmp_path):
        """Se o JSON for editado externamente com duplicatas, o app não pode mostrar erros."""
        filepath = str(tmp_path / "collections.json")
        dados_corrompidos = {
            "Laser": ["/path/a", "/path/a", "/path/a"]  # triplicado
        }
        with open(filepath, "w") as f:
            json.dump(dados_corrompidos, f)
        cm = CollectionsManager(file_path=filepath)
        projetos = cm.get_projects("Laser")
        assert projetos.count("/path/a") == 1, (
            "BUG: collections.json com entradas duplicadas não é sanitizado no load. "
            f"'/path/a' aparece {projetos.count('/path/a')}x na coleção."
        )


# ══════════════════════════════════════════════════════════════
# CORRUPÇÃO DO ARQUIVO
# ══════════════════════════════════════════════════════════════

class TestCorrupcao:

    def test_collections_json_com_lista_em_vez_de_dict(self, tmp_path):
        """Se o arquivo vier com [] em vez de {}, o app não pode travar."""
        filepath = str(tmp_path / "collections.json")
        with open(filepath, "w") as f:
            f.write("[]")  # formato errado
        cm = CollectionsManager(file_path=filepath)
        assert isinstance(cm.collections, dict), (
            "BUG: collections.json com '[]' (lista) vira cm.collections como lista. "
            "Qualquer operação de coleção vai quebrar com TypeError."
        )

    def test_collections_json_com_projeto_nao_string(self, tmp_path):
        """Projeto com valor não-string (ex: null, número) não pode quebrar is_project_in_collection."""
        filepath = str(tmp_path / "collections.json")
        dados = {"Laser": [None, 123, "/path/valido"]}
        with open(filepath, "w") as f:
            json.dump(dados, f)
        cm = CollectionsManager(file_path=filepath)
        try:
            resultado = cm.is_project_in_collection("Laser", "/path/valido")
            assert resultado is True
        except Exception as e:
            pytest.fail(f"BUG: dados inválidos no JSON travam is_project_in_collection: {e}")

    def test_arquivo_collections_sem_permissao_de_escrita(self, tmp_path):
        """Se o arquivo não puder ser salvo (disco cheio / permissão), não pode travar o app."""
        filepath = str(tmp_path / "collections.json")
        cm = CollectionsManager(file_path=filepath)
        cm.create_collection("Teste")
        # Torna a pasta read-only para simular falha de escrita
        os.chmod(str(tmp_path), 0o555)
        try:
            cm.save()  # não pode lançar exceção não tratada
        except PermissionError:
            pytest.fail("BUG: save() lança PermissionError não tratado — app trava.")
        finally:
            os.chmod(str(tmp_path), 0o755)  # restaura


# ══════════════════════════════════════════════════════════════
# CLEAN ORPHANS — remoção de projetos que não existem mais
# ══════════════════════════════════════════════════════════════

class TestCleanOrphans:

    def test_clean_orphans_com_valid_paths_none(self, cm):
        """clean_orphan_projects(None) não pode travar com TypeError."""
        cm.create_collection("Laser")
        cm.add_project("Laser", "/path/a")
        try:
            cm.clean_orphan_projects(None)
        except TypeError as e:
            pytest.fail(f"BUG: clean_orphan_projects(None) lança TypeError: {e}")

    def test_clean_orphans_com_valid_paths_lista_em_vez_de_set(self, cm):
        """valid_paths como lista em vez de set — pode ter comportamento diferente."""
        cm.create_collection("Laser")
        cm.add_project("Laser", "/path/a")
        cm.add_project("Laser", "/path/b")
        removidos = cm.clean_orphan_projects(["/path/a"])  # lista, não set
        assert removidos == 1, (
            f"BUG: clean_orphan_projects com lista retornou {removidos} em vez de 1. "
            "Aceita só set, não lista — inconsistência de tipo."
        )
        assert "/path/a" in cm.get_projects("Laser")
        assert "/path/b" not in cm.get_projects("Laser")
