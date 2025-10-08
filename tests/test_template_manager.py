import unittest
import os
import json
import shutil
from unittest.mock import patch

# Adiciona o caminho para encontrar os módulos da aplicação
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from conciliador.services import template_manager

class TestTemplateManager(unittest.TestCase):

    def setUp(self):
        """
        Configura um ambiente de teste limpo antes de cada teste.
        Cria um diretório de templates temporário.
        """
        self.test_dir = "temp_test_templates"
        # Usamos 'patch' para redirecionar o TEMPLATE_DIR do módulo para nosso diretório de teste
        self.patcher = patch('conciliador.services.template_manager.TEMPLATE_DIR', self.test_dir)
        self.patcher.start()
        # Garante que o diretório de teste não exista antes de começar
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        print(f"\n[SETUP] Test directory '{self.test_dir}' created for {self._testMethodName}")

    def tearDown(self):
        """
        Limpa o ambiente de teste após cada teste.
        Remove o diretório de templates temporário.
        """
        shutil.rmtree(self.test_dir)
        self.patcher.stop()
        print(f"[TEARDOWN] Test directory '{self.test_dir}' removed.")

    def test_save_template_success(self):
        """Testa se um template é salvo corretamente."""
        nome_template = "Meu Template Teste"
        mapping_template = {"data": "Data da Venda", "valor": "Total"}
        
        file_path = template_manager.save_template(nome_template, mapping_template)
        
        self.assertTrue(os.path.exists(file_path))
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(data['nome'], nome_template)
        self.assertEqual(data['mapping'], mapping_template)
        self.assertIn('data_criacao', data)

    def test_save_template_invalid_name(self):
        """Testa se o salvamento falha com um nome inválido."""
        with self.assertRaises(ValueError):
            template_manager.save_template("", {"data": "col1"})
        with self.assertRaises(ValueError):
            template_manager.save_template("   ", {"data": "col1"})

    def test_save_template_invalid_mapping(self):
        """Testa se o salvamento falha com um mapeamento inválido."""
        with self.assertRaises(ValueError):
            template_manager.save_template("Teste", {})
        with self.assertRaises(ValueError):
            template_manager.save_template("Teste", None)

    def test_load_template_success(self):
        """Testa o carregamento de um template existente."""
        nome_template = "Template para Carregar"
        mapping_template = {"data": "Data", "valor": "Valor", "tipo": "Tipo"}
        template_manager.save_template(nome_template, mapping_template)
        
        loaded_data = template_manager.load_template(nome_template)
        
        self.assertIsNotNone(loaded_data)
        self.assertEqual(loaded_data['nome'], nome_template)
        self.assertEqual(loaded_data['mapping'], mapping_template)

    def test_load_template_not_found(self):
        """Testa o carregamento de um template que não existe."""
        loaded_data = template_manager.load_template("template_inexistente")
        self.assertIsNone(loaded_data)

    def test_list_templates_success(self):
        """Testa a listagem de templates existentes."""
        template_manager.save_template("Template B", {"data": "col1"})
        template_manager.save_template("Template A", {"data": "col2"})
        template_manager.save_template("Template C", {"data": "col3"})
        
        templates = template_manager.list_templates()
        
        self.assertEqual(len(templates), 3)
        # A função deve retornar a lista ordenada
        self.assertEqual(templates, ["Template A", "Template B", "Template C"])

    def test_list_templates_empty(self):
        """Testa a listagem quando não há templates."""
        templates = template_manager.list_templates()
        self.assertEqual(templates, [])

    def test_delete_template_success(self):
        """Testa a exclusão de um template existente."""
        nome_template = "Template para Deletar"
        file_path = template_manager.save_template(nome_template, {"data": "col"})
        
        self.assertTrue(os.path.exists(file_path))
        
        result = template_manager.delete_template(nome_template)
        
        self.assertTrue(result)
        self.assertFalse(os.path.exists(file_path))

    def test_delete_template_not_found(self):
        """Testa a exclusão de um template que não existe."""
        result = template_manager.delete_template("template_inexistente")
        self.assertFalse(result)

    def test_filename_sanitization(self):
        """Testa se o nome do arquivo é sanitizado corretamente."""
        nome_template = "Template Com Espaços E MAIÚSCULAS"
        file_path = template_manager.save_template(nome_template, {"data": "col"})
        
        expected_filename = "template_com_espaços_e_maiúsculas.json"
        self.assertTrue(file_path.endswith(expected_filename))


if __name__ == '__main__':
    unittest.main(verbosity=2)