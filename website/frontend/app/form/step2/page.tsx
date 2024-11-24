'use client'; // Indique que ce fichier est un composant côté client

import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { useRouter } from 'next/navigation'; // Importation du hook useRouter
import { saveToLocalStorage } from '@/utils/localStorageHelper'; // Importation du helper pour le localStorage

const Step2 = () => {
  const [email, setEmail] = useState('');
  const router = useRouter(); // Hook pour la navigation

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Email soumis:', email);

    // Sauvegarder l'email dans le localStorage
    saveToLocalStorage('email', email);

    // Rediriger vers l'étape suivante
    router.push('/form/step3'); 
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <h1 className="text-2xl font-bold text-center mb-6">Quel est votre email ?</h1>
      <form onSubmit={handleSubmit}>
        <Input 
          type="email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
          placeholder="Entrez votre email"
          className="w-full"
        />
        <Button type="submit" className="w-full">Soumettre</Button>
      </form>
    </div>
  );
};

export default Step2;
