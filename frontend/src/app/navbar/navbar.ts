import { Component } from '@angular/core';
import { Search } from './search/search';

@Component({
  selector: 'app-navbar',
  imports: [Search],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css'
})
export class Navbar {

}
