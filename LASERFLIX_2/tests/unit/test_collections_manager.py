"""
tests/unit/test_collections_manager.py — Testes de comportamento do CollectionsManager.

Metodologia Akita:
- Testa regras de negocio reais, nao estrutura
- Usa tmp_collections do conftest (arquivo temporario isolado)
- Cada teste pode falhar por razao especifica e documentada
"""
import pytest


# ── CRUD de Colecoes ─────────────────────────────────────────────────────────

class TestCRUDColecoes:

    def test_criar_colecao_sucesso(self, tmp_collections):
        """Criar colecao com nome valido deve retornar True e aparecer na lista."""
        result = tmp_collections.create_collection("Filmes de Natal")
        assert result is True
        assert "Filmes de Natal" in tmp_collections.get_all_collections()

    def test_criar_colecao_duplicada_retorna_false(self, tmp_collections):
        """Criar colecao com nome que ja existe deve retornar False."""
        tmp_collections.create_collection("Favoritos")
        result = tmp_collections.create_collection("Favoritos")
        assert result is False

    def test_criar_colecao_nome_vazio_retorna_false(self, tmp_collections):
        """Nome vazio nao deve criar colecao."""
        assert tmp_collections.create_collection("") is False

    def test_criar_colecao_apenas_espacos_retorna_false(self, tmp_collections):
        """Nome com apenas espacos nao deve criar colecao."""
        assert tmp_collections.create_collection("   ") is False

    def test_add_collection_alias_funciona(self, tmp_collections):
        """add_collection e create_collection devem ter comportamento identico."""
        result = tmp_collections.add_collection("Via Alias")
        assert result is True
        assert "Via Alias" in tmp_collections.get_all_collections()

    def test_renomear_colecao(self, tmp_collections):
        """Renomear colecao existente: novo nome deve existir, antigo nao."""
        tmp_collections.create_collection("Antigo")
        result = tmp_collections.rename_collection("Antigo", "Novo")
        assert result is True
        assert "Novo" in tmp_collections.get_all_collections()
        assert "Antigo" not in tmp_collections.get_all_collections()

    def test_renomear_inexistente_retorna_false(self, tmp_collections):
        """Renomear colecao que nao existe deve retornar False."""
        assert tmp_collections.rename_collection("fantasma", "qualquer") is False

    def test_renomear_para_nome_existente_retorna_false(self, tmp_collections):
        """Renomear para nome que ja esta em uso deve retornar False."""
        tmp_collections.create_collection("A")
        tmp_collections.create_collection("B")
        assert tmp_collections.rename_collection("A", "B") is False

    def test_deletar_colecao(self, tmp_collections):
        """Deletar colecao existente deve retornar True e remove-la da lista."""
        tmp_collections.create_collection("Para Deletar")
        result = tmp_collections.delete_collection("Para Deletar")
        assert result is True
        assert "Para Deletar" not in tmp_collections.get_all_collections()

    def test_deletar_inexistente_retorna_false(self, tmp_collections):
        """Deletar colecao que nao existe deve retornar False sem explodir."""
        assert tmp_collections.delete_collection("nao_existe") is False

    def test_get_all_collections_ordenada(self, tmp_collections):
        """get_all_collections deve retornar lista ordenada alfabeticamente."""
        tmp_collections.create_collection("Zorro")
        tmp_collections.create_collection("Abelha")
        tmp_collections.create_collection("Meio")
        result = tmp_collections.get_all_collections()
        assert result == sorted(result)


# ── Gestao de Projetos ───────────────────────────────────────────────────────

class TestGestaoProjects:

    def test_add_project_sucesso(self, tmp_collections):
        """Adicionar projeto a colecao existente deve retornar True."""
        tmp_collections.create_collection("Col1")
        result = tmp_collections.add_project("Col1", "/path/proj1")
        assert result is True
        assert "/path/proj1" in tmp_collections.get_projects("Col1")

    def test_add_project_duplicado_retorna_false(self, tmp_collections):
        """Adicionar mesmo projeto duas vezes deve retornar False na segunda."""
        tmp_collections.create_collection("Col1")
        tmp_collections.add_project("Col1", "/path/proj1")
        result = tmp_collections.add_project("Col1", "/path/proj1")
        assert result is False

    def test_add_project_colecao_inexistente_retorna_false(self, tmp_collections):
        """Adicionar projeto a colecao que nao existe deve retornar False."""
        assert tmp_collections.add_project("fantasma", "/path/proj") is False

    def test_remove_project_sucesso(self, tmp_collections):
        """Remover projeto que existe na colecao deve retornar True e sumir."""
        tmp_collections.create_collection("Col1")
        tmp_collections.add_project("Col1", "/path/proj1")
        result = tmp_collections.remove_project("Col1", "/path/proj1")
        assert result is True
        assert "/path/proj1" not in tmp_collections.get_projects("Col1")

    def test_remove_project_ausente_retorna_false(self, tmp_collections):
        """Remover projeto que nao esta na colecao deve retornar False."""
        tmp_collections.create_collection("Col1")
        assert tmp_collections.remove_project("Col1", "/nao/esta") is False

    def test_is_project_in_collection_true(self, tmp_collections):
        """is_project_in_collection retorna True quando projeto esta na colecao."""
        tmp_collections.create_collection("Col1")
        tmp_collections.add_project("Col1", "/p")
        assert tmp_collections.is_project_in_collection("Col1", "/p") is True

    def test_is_project_in_collection_false(self, tmp_collections):
        """is_project_in_collection retorna False quando projeto nao esta."""
        tmp_collections.create_collection("Col1")
        assert tmp_collections.is_project_in_collection("Col1", "/nao") is False

    def test_get_project_collections_multiplas(self, tmp_collections):
        """Projeto em 3 colecoes: get_project_collections deve retornar as 3."""
        for nome in ["Col1", "Col2", "Col3"]:
            tmp_collections.create_collection(nome)
            tmp_collections.add_project(nome, "/path/proj")
        result = tmp_collections.get_project_collections("/path/proj")
        assert sorted(result) == ["Col1", "Col2", "Col3"]

    def test_get_project_collections_vazio(self, tmp_collections):
        """Projeto que nao esta em nenhuma colecao deve retornar lista vazia."""
        result = tmp_collections.get_project_collections("/nao/esta")
        assert result == []

    def test_get_collection_size(self, tmp_collections):
        """get_collection_size deve refletir numero real de projetos."""
        tmp_collections.create_collection("Col1")
        assert tmp_collections.get_collection_size("Col1") == 0
        tmp_collections.add_project("Col1", "/a")
        tmp_collections.add_project("Col1", "/b")
        assert tmp_collections.get_collection_size("Col1") == 2


# ── Utilitarios ──────────────────────────────────────────────────────────────

class TestUtilitarios:

    def test_clean_orphan_projects(self, tmp_collections):
        """clean_orphan_projects deve remover paths que nao estao em valid_paths."""
        tmp_collections.create_collection("Col1")
        for i in range(5):
            tmp_collections.add_project("Col1", f"/path/{i}")
        # Apenas /path/0 e /path/1 sao validos
        removed = tmp_collections.clean_orphan_projects({"/path/0", "/path/1"})
        assert removed == 3
        assert tmp_collections.get_collection_size("Col1") == 2

    def test_clean_orphan_sem_orfaos_retorna_zero(self, tmp_collections):
        """Sem orfaos, clean_orphan_projects deve retornar 0."""
        tmp_collections.create_collection("Col1")
        tmp_collections.add_project("Col1", "/valido")
        removed = tmp_collections.clean_orphan_projects({"/valido"})
        assert removed == 0

    def test_get_stats_correto(self, tmp_collections):
        """get_stats deve reportar total_collections e unique_projects corretamente."""
        tmp_collections.create_collection("A")
        tmp_collections.create_collection("B")
        tmp_collections.add_project("A", "/proj1")
        tmp_collections.add_project("A", "/proj2")
        tmp_collections.add_project("B", "/proj1")  # Mesmo proj em 2 colecoes
        stats = tmp_collections.get_stats()
        assert stats["total_collections"] == 2
        assert stats["unique_projects"] == 2  # /proj1 e /proj2
        assert stats["total_entries"] == 3    # contagem total (com repeticao)

    def test_save_e_reload_roundtrip(self, tmp_path):
        """Colecoes criadas devem persistir e ser recuperadas em nova instancia."""
        from core.collections_manager import CollectionsManager
        col_file = str(tmp_path / "collections.json")

        cm1 = CollectionsManager(file_path=col_file)
        cm1.create_collection("Natal")
        cm1.add_project("Natal", "/path/proj_natal")

        cm2 = CollectionsManager(file_path=col_file)
        assert "Natal" in cm2.get_all_collections()
        assert "/path/proj_natal" in cm2.get_projects("Natal")

    def test_load_json_corrompido_inicia_vazio(self, tmp_path):
        """JSON corrompido nao deve explodir: inicia com collections vazio."""
        from core.collections_manager import CollectionsManager
        col_file = tmp_path / "collections.json"
        col_file.write_text("{ json corrompido ]]]")
        cm = CollectionsManager(file_path=str(col_file))
        assert cm.get_all_collections() == []
