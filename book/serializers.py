
from rest_framework import serializers

from .models import Ledger, Entry


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        exclude = ('user', 'ledgers')


class LedgerSerializer(serializers.ModelSerializer):
    
    # entries = EntrySerializer(many=True, read_only=True)

    class Meta:
        model = Ledger
        exclude = ('user',)
        # fields = ('id', 'title', 'icon', 'date_created', 'description', 'entries')