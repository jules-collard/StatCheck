import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShootingTable } from './shooting-table';

describe('ShootingTable', () => {
  let component: ShootingTable;
  let fixture: ComponentFixture<ShootingTable>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ShootingTable]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ShootingTable);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
