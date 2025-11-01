import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Scorebug } from './scorebug';

describe('Scorebug', () => {
  let component: Scorebug;
  let fixture: ComponentFixture<Scorebug>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Scorebug]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Scorebug);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
