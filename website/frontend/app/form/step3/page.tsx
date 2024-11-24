'use client'; // Indique que ce fichier est un composant côté client

import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { useRouter } from 'next/navigation'; // Importation du hook useRouter
import { saveToLocalStorage } from '@/utils/localStorageHelper'; // Importation du helper pour le localStorage

const Step3 = () => {
  const [phone, setPhone] = useState('');
  const router = useRouter(); // Hook pour la navigation

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Téléphone soumis:', phone);

    // Sauvegarder le numéro de téléphone dans le localStorage
    saveToLocalStorage('phone', phone);

    // Rediriger vers la page de succès
    router.push('/form/success');
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <h1 className="text-2xl font-bold text-center mb-6">Quel est votre numéro de téléphone ?</h1>
      <form onSubmit={handleSubmit}>
        <Input 
          type="tel" 
          value={phone} 
          onChange={(e) => setPhone(e.target.value)} 
          placeholder="Entrez votre numéro de téléphone"
          className="w-full"
        />
        <Button type="submit" className="w-full">Soumettre</Button>
      </form>
    </div>
  );
};

export default Step3;
