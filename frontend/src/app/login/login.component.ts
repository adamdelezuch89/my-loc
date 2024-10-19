import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { UserInterface } from '../user.interface';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  standalone: true,
  imports: [ReactiveFormsModule],
})
export class LoginComponent { // changed to LoginComponent
  fb = inject(FormBuilder);
  http = inject(HttpClient);
  authService = inject(AuthService);
  router = inject(Router);

  form = this.fb.nonNullable.group({
    email: ['', Validators.required],
    password: ['', Validators.required],
  });

  onSubmit(): void {
    
    this.http
      .post<{ token: string }>(
        'http://localhost:8000/api/user/token/', 
        this.form.getRawValue()
      )
      .subscribe((response) => {

        console.log('token handled');
        localStorage.setItem('token', response.token);
        console.log(response);
        this.http
          .get<{ name: string, email: string }>('http://localhost:8000/api/user/me/')
          .subscribe((userData) => {
            console.log('User data', userData);

            const user: UserInterface = {
              email: userData.email,
              token: response.token,
              name: userData.name,
            };

            this.authService.currentUserSig.set(user);
            this.router.navigateByUrl('/');
          });
      });
  }
}