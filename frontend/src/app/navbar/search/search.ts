import { Component, inject, output } from '@angular/core';
import { FormsModule } from '@angular/forms'
import { Router } from '@angular/router';

@Component({
  selector: 'app-search',
  imports: [FormsModule],
  templateUrl: './search.html',
  styleUrl: './search.css'
})
export class Search {
  private router = inject(Router)
  enteredPlayerName = '';

  onFindPlayer() {
    this.router.navigate(['search'], {
      queryParams: {
        q: this.enteredPlayerName
      }
    })
  }
}
