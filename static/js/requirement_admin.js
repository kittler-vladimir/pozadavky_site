// requirement_admin.js
document.addEventListener('DOMContentLoaded', function() {
    const groupSelect = document.getElementById('id_group_owner');
    const ownerSelect = document.getElementById('id_owner');

    if (!groupSelect || !ownerSelect) return;

    groupSelect.addEventListener('change', function() {
        const groupId = this.value;
        ownerSelect.innerHTML = '<option value="">Načítám...</option>';

        if (!groupId) {
            ownerSelect.innerHTML = '<option value="">-- Vyberte vlastníka --</option>';
            return;
        }

        fetch(`/admin/pozadavky/requirement/get_owners/?group_id=${groupId}`)
            .then(response => {
                if (!response.ok) throw new Error('Síťová chyba');
                return response.json();
            })
            .then(data => {
                ownerSelect.innerHTML = '<option value="">-- Vyberte vlastníka --</option>';
                data.forEach(user => {
                    const option = document.createElement('option');
                    option.value = user.id;
                    option.textContent = user.name; // celé jméno z API
                    ownerSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Chyba při načítání vlastníků:', error);
                ownerSelect.innerHTML = '<option value="">Chyba při načítání</option>';
            });
    });
});
