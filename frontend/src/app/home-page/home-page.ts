import { Component } from '@angular/core';
import { Scorebug } from "./scorebug/scorebug";

@Component({
  selector: 'app-home-page',
  imports: [Scorebug],
  templateUrl: './home-page.html',
  styleUrl: './home-page.css'
})
export class HomePage {

}
