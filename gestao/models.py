# gestao/models.py

from django.db import models

class Terreiro(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    documento = models.CharField(max_length=15, verbose_name="Documento (CNPJ)")
    email = models.EmailField(null=False, verbose_name="E-mail")
    telefone = models.CharField(max_length=15, verbose_name="Telefone")
    data_fundacao = models.DateField(verbose_name="Data de Fundação")
    rua = models.CharField(max_length=255, verbose_name="Rua")
    numero = models.CharField(max_length=10, verbose_name="Número")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(max_length=2, verbose_name="Estado")
    cep = models.CharField(max_length=10, verbose_name="CEP")

    class Meta:
        verbose_name = "Terreiro"

    def __str__(self):
        return self.nome


class Cargo(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    terreiro = models.ForeignKey(
        'Terreiro',  # Referência ao modelo Terreiro
        on_delete=models.CASCADE,
        related_name="cargos",
        verbose_name="Terreiro"
    )

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        app_label = 'gestao'

    def __str__(self):
        return self.nome


class Hierarquia(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    terreiro = models.ForeignKey(
        'Terreiro',  # Referência ao modelo Terreiro
        on_delete=models.CASCADE,
        related_name="hierarquias",
        verbose_name="Terreiro"
    )

    class Meta:
        verbose_name = "Hierarquia"
        verbose_name_plural = "Hierarquias"

    def __str__(self):
        return self.nome



class Mediun(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    sobrenome = models.CharField(max_length=100, verbose_name="Sobrenome")
    documento = models.CharField(max_length=14, verbose_name="Documento (CPF)", blank=True, null=True)
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    email = models.EmailField(verbose_name="E-mail")
    telefone = models.CharField(max_length=15, verbose_name="Telefone")
    cargos = models.ForeignKey(
        Cargo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cargo"
    )
    hierarquia = models.ForeignKey(
        Hierarquia, on_delete=models.CASCADE, verbose_name="Hierarquia"
    )
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Mediun"
        verbose_name_plural = "Médiuns"

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"


class CaminhadaEspiritual(models.Model):
    mediun = models.OneToOneField(
        Mediun, on_delete=models.CASCADE, related_name="caminhada_espiritual"
    )
    data_entrada = models.DateField(verbose_name="Data de Entrada")
    data_batismo = models.DateField(verbose_name="Data de Batismo", null=True, blank=True)
    data_obori = models.DateField(verbose_name="Data de Obori", null=True, blank=True)
    data_pai_mae_pequeno = models.DateField(verbose_name="Data Pai/Mãe Pequeno", null=True, blank=True)
    data_baba_ya = models.DateField(verbose_name="Data Babá Ya", null=True, blank=True)
    data_reforco7 = models.DateField(verbose_name="Data Reforço 7 Anos", null=True, blank=True)
    data_reforco14 = models.DateField(verbose_name="Data Reforço 14 Anos", null=True, blank=True)
    data_reforco21 = models.DateField(verbose_name="Data Reforço 21 Anos", null=True, blank=True)
    data_desligamento = models.DateField(verbose_name="Data de Desligamento", null=True, blank=True)

    class Meta:
        verbose_name = "Caminhada Espiritual"

    def __str__(self):
        return f"Registro de {self.mediun.nome} - {self.data_entrada}"


class RegistroEspiritual(models.Model):
    mediun = models.OneToOneField(
        Mediun, on_delete=models.CASCADE, related_name="registro_espiritual"
    )
    primeiro_santo = models.CharField(max_length=100, null=True, blank=True, verbose_name="Primeiro Santo")
    segundo_santo = models.CharField(max_length=100, null=True, blank=True, verbose_name="Segundo Santo")
    exu = models.CharField(max_length=100, null=True, blank=True, verbose_name="Exu")
    pomba_gira = models.CharField(max_length=100, null=True, blank=True, verbose_name="Pomba Gira")
    preto_velho = models.CharField(max_length=100, null=True, blank=True, verbose_name="Preto Velho")
    caboclo = models.CharField(max_length=100, null=True, blank=True, verbose_name="Caboclo")
    ibeijada = models.CharField(max_length=100, null=True, blank=True, verbose_name="Ibeijada")
    responsavel_coroa = models.CharField(max_length=100, null=True, blank=True, verbose_name="Responsável anjo de guarda")
    padrinho_espiritual= models.CharField(max_length=100, null=True, blank=True, verbose_name="Padrinho Espiritual")
    madrinha_espiritual = models.CharField(max_length=100, null=True, blank=True, verbose_name="Madrinha Espiritual")
    padrinho_batismo = models.CharField(max_length=100, null=True, blank=True, verbose_name="Padrinho Batismo")
    madrinha_batismo = models.CharField(max_length=100, null=True, blank=True, verbose_name="Madrinha Batismo")

    class Meta:
        verbose_name = "Registro Espiritual"
        verbose_name_plural = "Registros Espirituais"

    def __str__(self):
        return f"Registro de {self.mediun.nome}"


class Mensalidade(models.Model):
    mediun = models.ForeignKey(
        Mediun, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Mediun"
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor R$:")
    data_vencimento = models.DateField(verbose_name="Data de Vencimento")
    paga = models.BooleanField(default=False, verbose_name="Paga")

    class Meta:
        verbose_name = "Mensalidade"
        verbose_name_plural = "Mensalidades"

    def __str__(self):
        return f"Mensalidade de {self.mediun.nome if self.mediun else 'Sem Mediun'}"


class Evento(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    data = models.DateTimeField(verbose_name="Data")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return self.titulo

class Item(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Itens"

    def __str__(self):
        return self.nome

class DistribuicaoItens(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    mediun = models.ForeignKey(Mediun, on_delete=models.CASCADE)
    data_distribuicao = models.DateField(default='2023-01-01')  # Data da distribuição

    class Meta:
        verbose_name ="Distribuição de Iten"

    def __str__(self):
        return f"{self.mediun.nome} = {self.item.nome}"
