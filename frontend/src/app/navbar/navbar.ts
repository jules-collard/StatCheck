import { Component, inject } from '@angular/core';
import { Search } from './search/search';
import { RouterLink } from '@angular/router';
import { GlobalConfigService } from '../shared/global-config.service';

@Component({
  selector: 'app-navbar',
  imports: [Search, RouterLink],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css'
})
export class Navbar {
  config = inject(GlobalConfigService)
}
