import { Component, computed, input } from '@angular/core';

@Component({
  selector: 'app-award-badge',
  imports: [],
  templateUrl: './award-badge.html',
  styleUrl: './award-badge.css'
})
export class AwardBadge {
  award = input.required<string>();
  
  class = computed(() => {
    if (this.award() == "Stanley Cup") {
      return "badge badge-warning badge-sm";
    } else if (this.award() === "Hart Memorial Trophy") {
      return "badge badge-secondary badge-sm";
    } else {
      return "badge badge-soft badge-accent";
    }
  });

  text = computed(() => {
    if (this.award() == "Hart Memorial Trophy") {
      return "MVP";
    } else if (this.award() == "James Norris Memorial Trophy") {
      return "Norris";
    } else if (this.award() == "Frank J. Selke Trophy") {
      return "Selke"
    } else {
      return this.award().replace('Trophy', '').replace('Memorial', '').trim()
    }
  });
}
