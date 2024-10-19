import { Injectable, signal, inject } from '@angular/core';
import { UserInterface } from './user.interface';
import { HttpClient } from '@angular/common/http';
@Injectable({
  providedIn: 'root',
})
export class AuthService {
  currentUserSig = signal<UserInterface | undefined | null>(undefined);
  token: string = localStorage.getItem('token') || '';
  http = inject(HttpClient);
  constructor() {
    if (this.token) {
      this.http
      .get<{  email: string; name: string  }>('http://localhost:8000/api/user/me')
      .subscribe({
        next: (response) => {
          console.log('response', response);
          const user: UserInterface = {
            email: response.email,
            token: this.token,
            name: response.name,
          };

          this.currentUserSig.set(user);
        },
        error: () => {
          this.currentUserSig.set(null);
        },
      });
    }
  }
}
