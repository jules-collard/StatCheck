import { Component } from '@angular/core';
import { Search } from './search/search';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-navbar',
  imports: [Search, RouterLink],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css'
})
export class Navbar {

}
