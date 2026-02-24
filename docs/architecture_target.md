# Arquitetura alvo (WhatsApp + SQS + Insights)

## Princípios
- Domínio isolado de framework/SDK externo.
- Mensagens da fila versionadas e com contrato explícito.
- Worker idempotente com rastreabilidade por `message_id`.
- Serviços de IA encapsulados em infraestrutura.

## Contrato de mensagem SQS

```json
{
  "message_id": "uuid",
  "event_type": "invoice.uploaded | whatsapp.message.received",
  "user_id": 1,
  "payload": {},
  "occurred_at": "2026-01-01T00:00:00Z",
  "schema_version": "1.0"
}
```

## Fluxo recomendado
1. Webhook/API valida entrada.
2. API transforma em evento de domínio e publica envelope na SQS.
3. Worker consome, grava `processing_status=processing`.
4. Worker executa use case adequado por `event_type`.
5. Em sucesso, marca `done`; em erro, marca `failed`.

## Escalabilidade
- Aumentar número de workers horizontalmente sem alterar regras de negócio.
- Idempotência por `message_id` evita duplicidade.
- `VisibilityTimeout` maior que tempo médio de processamento.
- DLQ para mensagens com falha recorrente.

## Insights com IA (Bedrock)
- `BedrockService` restrito à infraestrutura.
- Use case de insights monta prompt com agregações mensais.
- Persistir resultado em `insights` com referência de mês.
- Implementar cache mensal para não recalcular no mesmo período.

## Modelo mínimo de tabelas
- `transactions`
- `categories`
- `category_rules`
- `processing_status`
- `insights`
- `financial_goals`
