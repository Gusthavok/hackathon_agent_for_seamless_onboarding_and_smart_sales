'use client';  // Cette ligne indique que ce composant est un Client Component

import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { useRouter } from 'next/navigation';  // Importation du hook useRouter
import { saveToLocalStorage } from '@/utils/localStorageHelper'; // Importation du helper pour le localStorage

const Step1 = () => {
  const [name, setName] = useState('');
  const router = useRouter(); // Maintenant, ce hook fonctionne côté client

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Nom soumis:', name);

    // Sauvegarder le nom dans le localStorage
    saveToLocalStorage('name', name);

    // Exemple de redirection après soumission
    router.push('/form/step2'); // Redirection vers l'étape suivante
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <h1 className="text-2xl font-bold text-center mb-6">Quel est votre prénom ?</h1>
      <form onSubmit={handleSubmit}>
        <Input 
          type="text" 
          value={name} 
          onChange={(e) => setName(e.target.value)} 
          placeholder="Entrez votre prénom"
          className="w-full"
        />
        <Button type="submit" className="w-full">Soumettre</Button>
      </form>
    </div>
  );
};

export default Step1;
