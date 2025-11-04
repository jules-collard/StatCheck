import { Component, input } from '@angular/core';
import { StandingsItem } from '../standings-item.model';
import { DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-standings',
  imports: [DecimalPipe],
  templateUrl: './standings.html',
  styleUrl: './standings.css'
})
export class Standings {
  teams = input.required<StandingsItem[]>();
}
