from django.contrib import admin
from .models import Cargo, Hierarquia, Mediun, Mensalidade, Evento, CaminhadaEspiritual, Terreiro, RegistroEspiritual
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import ExtractMonth
import csv
from django.http import HttpResponse



class CargoInline(admin.TabularInline):  # Herda de TabularInline
    model = Cargo
    extra = 1  # Mostrar pelo menos 1 campo vazio para adicionar novos cargos

class HierarquiaInline(admin.TabularInline):  # Herda de TabularInline
    model = Hierarquia
    extra = 1  # Mostrar pelo menos 1 campo vazio para adicionar novas hierarquias


class CaminhadaEspiritualInline(admin.StackedInline):  # ou admin.StackedInline
    model = CaminhadaEspiritual
    max_num = 1  # Apenas 1 por médium

class RegistroEspiritualInLine(admin.StackedInline):
    model = RegistroEspiritual
    max_num = 1 # Apenas 1 por Médiun


class AniversariantesMesFilter(admin.SimpleListFilter):
    """Filtro para listar médiuns aniversariantes por mês"""
    title = _('Mês de Aniversário')
    parameter_name = 'data_nascimento'

    def lookups(self, request, model_admin):
        """Define os valores dos meses no filtro"""
        meses = [
            (1, _('Janeiro')), (2, _('Fevereiro')), (3, _('Março')),
            (4, _('Abril')), (5, _('Maio')), (6, _('Junho')),
            (7, _('Julho')), (8, _('Agosto')), (9, _('Setembro')),
            (10, _('Outubro')), (11, _('Novembro')), (12, _('Dezembro')),
        ]
        return meses

    def queryset(self, request, queryset):
        """Filtra os médiuns pelo mês selecionado"""
        if self.value():
            return queryset.annotate(
                mes_aniversario=ExtractMonth('data_nascimento')
            ).filter(mes_aniversario=self.value())
        return queryset


@admin.register(Mediun)
class MediunAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Dados Básicos", {
            "fields": (
                "nome", "sobrenome", "data_nascimento", "documento", "telefone", "email",
                "cargos", "hierarquia", "is_active"),  # Organizando campos
        }),
    )
    inlines = [CaminhadaEspiritualInline, RegistroEspiritualInLine]  # Inline para relação com caminhada espiritual
    list_display = ("nome", "sobrenome", "cargos", "hierarquia", "is_active")  # Listagem personalizada
    list_filter = ("cargos", "is_active", AniversariantesMesFilter)  # Filtros laterais

    # Função usada para exportar os dados selecionados para CSV
    def exportar_csv(self, request, queryset):
        # Define o tipo do response como CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="mediuns_exportados.csv"'

        # Cria o escritor CSV
        writer = csv.writer(response)
        # Define os cabeçalhos das colunas do CSV
        writer.writerow(
            ['Nome', 'Sobrenome', 'Data de Nascimento', 'Documento', 'Telefone', 'Email', 'Cargos', 'Hierarquia',
             'Ativo'])

        # Itera pelos objetos selecionados e escreve as linhas no CSV
        for mediun in queryset:
            writer.writerow([
                mediun.nome,
                mediun.sobrenome,
                mediun.data_nascimento,
                mediun.documento,
                mediun.telefone,
                mediun.email,
                mediun.cargos.nome if mediun.cargos else "",  # Obtem nome do cargo se existir
                mediun.hierarquia.nome if mediun.hierarquia else "",  # Obtem o nome da hierarquia se existir
                "Sim" if mediun.is_active else "Não"
            ])

        return response

    # Atribui um nome amigável à ação
    exportar_csv.short_description = "Exportar Médiuns selecionados para CSV"

    # Lista de ações disponíveis no Django Admin
    actions = [exportar_csv]


@admin.register(Mensalidade)
class MensalidadeAdmin(admin.ModelAdmin):
    list_display = ('mediun', 'valor', 'data_vencimento', 'paga')  # Exibe valores principais
    list_filter = ('paga', 'data_vencimento')  # Filtros


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data')  # Exibe os campos principais


@admin.register(Terreiro)
class TerreiroAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Dados Básicos", {
            "fields": (
                "nome","documento", "email", "telefone", "data_fundacao", "cep", "rua", "numero", "bairro", "cidade", "estado")  # Campos a serem exibidos na aba "Dados Básicos"
        }),
    )
    inlines = [CargoInline, HierarquiaInline]  # Usar classes inlines definidas corretamente
    list_display = ('nome', 'data_fundacao', 'email')  # Listagem no painel
    search_fields = ('nome', 'email')  # Pesquisa habilitada pelos campos 'nome' e 'email'


